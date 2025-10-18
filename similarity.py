import os
import numpy as np
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from sklearn.metrics.pairwise import cosine_similarity

# Initialize FastAPI app
app = FastAPI(title="InfoCore Semantic Search API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["OPTIONS", "POST", "GET"],  # Allow OPTIONS and POST
    allow_headers=["*"],  # Allow all headers
)

# Add OPTIONS handler for preflight requests
@app.options("/similarity")
async def options_similarity():
    """Handle CORS preflight requests for /similarity endpoint"""
    return {"message": "OK"}

# Pydantic models for request/response
class SearchRequest(BaseModel):
    docs: List[str]
    query: str

class SearchResponse(BaseModel):
    matches: List[str]

# Set OpenAI API key (you'll need to set this environment variable)
# openai.api_key = os.getenv("OPENAI_API_KEY")

# For demo purposes, we'll use a simple embedding function
# In production, you would use OpenAI's text-embedding-3-small
def get_text_embedding(text: str) -> List[float]:
    """
    Generate text embedding using a simple TF-IDF-like approach.
    In production, you would use OpenAI's text-embedding-3-small model.
    """
    # In production, uncomment this:
    # try:
    #     response = openai.embeddings.create(
    #         model="text-embedding-3-small",
    #         input=text
    #     )
    #     return response.data[0].embedding
    # except Exception as e:
    #     raise HTTPException(status_code=500, f"Error generating embedding: {str(e)}")
    
    # Simple demo embedding using word frequency and presence
    import re
    
    # Clean and tokenize text
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    # Define important keywords for different domains
    keywords = [
        'machine', 'learning', 'ai', 'artificial', 'intelligence', 'neural', 'network', 'algorithm',
        'python', 'programming', 'code', 'language', 'development', 'software', 'computer',
        'data', 'science', 'analysis', 'database', 'sql', 'analytics', 'statistics',
        'web', 'javascript', 'react', 'html', 'css', 'frontend', 'backend', 'api',
        'cloud', 'computing', 'server', 'storage', 'aws', 'azure', 'infrastructure',
        'security', 'cybersecurity', 'protection', 'encryption', 'firewall', 'attack',
        'business', 'management', 'project', 'process', 'system', 'enterprise',
        'mobile', 'app', 'application', 'ios', 'android', 'user', 'interface'
    ]
    
    # Create embedding based on keyword presence and frequency
    embedding = []
    word_count = len(words)
    
    for keyword in keywords:
        # Count keyword frequency
        count = words.count(keyword)
        # Normalize by document length
        freq = count / word_count if word_count > 0 else 0
        embedding.append(freq)
    
    # Add some additional features based on text characteristics
    embedding.extend([
        len(words) / 100.0,  # Document length feature
        len(set(words)) / len(words) if len(words) > 0 else 0,  # Vocabulary diversity
        sum(1 for w in words if len(w) > 6) / len(words) if len(words) > 0 else 0,  # Complex words ratio
    ])
    
    # Pad or truncate to fixed size
    target_size = 50
    if len(embedding) < target_size:
        embedding.extend([0.0] * (target_size - len(embedding)))
    else:
        embedding = embedding[:target_size]
    
    return embedding

def compute_cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Compute cosine similarity between two embeddings."""
    # Convert to numpy arrays
    vec1 = np.array(embedding1).reshape(1, -1)
    vec2 = np.array(embedding2).reshape(1, -1)
    
    # Compute cosine similarity
    similarity = cosine_similarity(vec1, vec2)[0][0]
    return float(similarity)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "InfoCore Semantic Search API",
        "endpoints": {
            "/similarity": "POST endpoint for semantic document search"
        }
    }

@app.post("/similarity", response_model=SearchResponse)
async def semantic_search(request: SearchRequest):
    """
    Semantic search endpoint that finds the most similar documents to a query.
    
    Args:
        request: SearchRequest containing docs array and query string
        
    Returns:
        SearchResponse with the top 3 most similar documents
    """
    try:
        if not request.docs:
            raise HTTPException(status_code=400, detail="No documents provided")
        
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Generate embedding for the query
        query_embedding = get_text_embedding(request.query)
        
        # Generate embeddings for all documents and compute similarities
        similarities = []
        for i, doc in enumerate(request.docs):
            if not doc.strip():
                continue  # Skip empty documents
                
            doc_embedding = get_text_embedding(doc)
            similarity = compute_cosine_similarity(query_embedding, doc_embedding)
            similarities.append((similarity, i, doc))
        
        if not similarities:
            raise HTTPException(status_code=400, detail="No valid documents found")
        
        # Sort by similarity (descending) and get top 3
        similarities.sort(key=lambda x: x[0], reverse=True)
        top_matches = similarities[:3]
        
        # Extract the document contents for the response
        matches = [doc for _, _, doc in top_matches]
        
        return SearchResponse(matches=matches)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)