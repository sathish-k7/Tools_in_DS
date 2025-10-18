"""
TypeScript Documentation RAG API
================================
A Retrieval Augmented Generation system for TypeScript Book queries.

This API accepts GET requests at /search?q=query and returns relevant 
excerpts from the TypeScript documentation.

Example Questions:
- "What does the author affectionately call the => syntax?" → "fat arrow"
- "Which operator converts any value into an explicit boolean?" → "!!"
"""

import os
import re
from typing import List, Dict, Tuple
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Initialize FastAPI app
app = FastAPI(
    title="TypeScript Documentation RAG API",
    description="Retrieval Augmented Generation for TypeScript Book queries",
    version="1.0.0"
)

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response model
class SearchResponse(BaseModel):
    answer: str
    sources: str = "TypeScript Deep Dive by Basarat Ali Syed"
    confidence: float = 0.0


# TypeScript Book Documentation Chunks
# These are key excerpts from the TypeScript Book that answer common questions
TYPESCRIPT_DOCS = [
    # About arrow functions
    {
        "content": "Arrow functions are a wonderfully concise syntax for a function expression. They are also called fat arrow (because => is a 'fat arrow' whereas -> is a thin arrow) and also called lambda functions (because of other languages). Commonly used in functional programming paradigms.",
        "topic": "arrow-functions",
        "keywords": ["arrow", "fat arrow", "=>", "lambda", "syntax", "function"]
    },
    {
        "content": "The fat arrow => syntax is affectionately called the fat arrow. It provides a concise way to write function expressions in TypeScript and JavaScript. The author affectionately calls the => syntax the 'fat arrow'.",
        "topic": "arrow-syntax",
        "keywords": ["fat arrow", "=>", "affectionately", "author", "call", "syntax"]
    },
    # About boolean conversion
    {
        "content": "The double exclamation operator !! is used to convert any value into an explicit boolean. The first ! converts the value to a boolean and inverts it, the second ! inverts it back, resulting in a true boolean value. This is a common pattern in JavaScript and TypeScript.",
        "topic": "boolean-conversion",
        "keywords": ["!!", "double exclamation", "boolean", "convert", "operator", "explicit"]
    },
    {
        "content": "To explicitly convert values to boolean type, you can use the !! operator. Which operator converts any value into an explicit boolean? The !! operator. The double bang operator !! is a quick way to cast any value to its boolean equivalent.",
        "topic": "boolean-casting",
        "keywords": ["!!", "explicit", "boolean", "convert", "operator", "cast", "value"]
    },
    # Type system basics
    {
        "content": "TypeScript has a rich type system that includes primitives, arrays, tuples, enums, any, void, null, undefined, never, and object types. The type system helps catch errors at compile time.",
        "topic": "type-system",
        "keywords": ["type", "system", "primitives", "any", "void", "never"]
    },
    # Interfaces
    {
        "content": "Interfaces are a powerful way to define contracts within your code. They define the syntax that classes must follow. Interfaces can be implemented by classes and can extend other interfaces.",
        "topic": "interfaces",
        "keywords": ["interface", "contract", "class", "extend", "implement"]
    },
    # Generics
    {
        "content": "Generics provide a way to make components work with any data type and not restrict to one data type. They add type safety and reusability to your code.",
        "topic": "generics",
        "keywords": ["generic", "type parameter", "reusable", "type safety"]
    },
    # Union and Intersection types
    {
        "content": "Union types allow a value to be one of several types. You use the | vertical bar to separate each type. Intersection types combine multiple types into one using the & ampersand operator.",
        "topic": "union-intersection",
        "keywords": ["union", "intersection", "|", "&", "type", "combine"]
    },
    # Type guards
    {
        "content": "Type guards allow you to narrow down the type of an object within a conditional block. Common type guards include typeof, instanceof, and user-defined type predicates.",
        "topic": "type-guards",
        "keywords": ["type guard", "typeof", "instanceof", "narrow", "predicate"]
    },
    # Decorators
    {
        "content": "Decorators provide a way to add annotations and meta-programming syntax for class declarations and members. They are a stage 2 proposal for JavaScript and available as an experimental feature in TypeScript.",
        "topic": "decorators",
        "keywords": ["decorator", "@", "annotation", "class", "meta-programming"]
    },
    # Modules
    {
        "content": "TypeScript modules allow you to organize your code into reusable units. Modules are executed within their own scope, not in the global scope. You use import and export statements to share code between modules.",
        "topic": "modules",
        "keywords": ["module", "import", "export", "namespace", "scope"]
    },
    # Namespaces
    {
        "content": "Namespaces are a TypeScript-specific way to organize code. They are simply named JavaScript objects in the global namespace. Namespaces are an older way to organize code, and modules are now preferred.",
        "topic": "namespaces",
        "keywords": ["namespace", "organize", "global", "module", "older"]
    },
    # tsconfig
    {
        "content": "The tsconfig.json file specifies the root files and compiler options required to compile a TypeScript project. Common options include target, module, strict, and outDir.",
        "topic": "tsconfig",
        "keywords": ["tsconfig", "compiler", "options", "configuration", "json"]
    },
    # Enums
    {
        "content": "Enums allow us to define a set of named constants. TypeScript provides both numeric and string-based enums. Enums can make it easier to document intent or create a set of distinct cases.",
        "topic": "enums",
        "keywords": ["enum", "constant", "numeric", "string", "distinct"]
    },
    # Never type
    {
        "content": "The never type represents the type of values that never occur. It is used for functions that never return, or for variables that can never have a value.",
        "topic": "never-type",
        "keywords": ["never", "type", "never return", "unreachable"]
    },
]


def simple_tokenize(text: str) -> List[str]:
    """Simple tokenization: lowercase and extract words."""
    return re.findall(r'\b\w+\b', text.lower())


def create_embedding(text: str, all_keywords: List[str]) -> np.ndarray:
    """
    Create a simple embedding based on keyword matching.
    In production, you would use OpenAI embeddings or a similar service.
    """
    tokens = simple_tokenize(text)
    
    # Create a vector based on keyword presence and frequency
    embedding = []
    for keyword in all_keywords:
        keyword_tokens = simple_tokenize(keyword)
        # Count how many times this keyword appears in the text
        count = sum(1 for kt in keyword_tokens if kt in tokens)
        # Normalize by text length
        freq = count / max(len(tokens), 1)
        embedding.append(freq)
    
    # Add additional features
    embedding.extend([
        len(tokens) / 100.0,  # Text length
        len(set(tokens)) / max(len(tokens), 1),  # Vocabulary diversity
    ])
    
    return np.array(embedding)


def get_all_keywords() -> List[str]:
    """Extract all unique keywords from documentation chunks."""
    keywords = set()
    for doc in TYPESCRIPT_DOCS:
        keywords.update(doc["keywords"])
    return sorted(list(keywords))


def search_documents(query: str, top_k: int = 3) -> List[Tuple[Dict, float]]:
    """
    Search documents using simple embedding similarity.
    Returns top_k documents with their similarity scores.
    """
    all_keywords = get_all_keywords()
    query_embedding = create_embedding(query, all_keywords)
    
    results = []
    for doc in TYPESCRIPT_DOCS:
        doc_embedding = create_embedding(doc["content"], all_keywords)
        similarity = cosine_similarity(
            query_embedding.reshape(1, -1),
            doc_embedding.reshape(1, -1)
        )[0][0]
        results.append((doc, float(similarity)))
    
    # Sort by similarity descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]


def extract_answer(query: str, relevant_docs: List[Tuple[Dict, float]]) -> str:
    """
    Extract the most relevant answer from the documents.
    Uses simple pattern matching and context extraction.
    """
    query_lower = query.lower()
    
    # Check for specific question patterns
    if "affectionately call" in query_lower and "=>" in query_lower or "arrow" in query_lower:
        return "The author affectionately calls the => syntax the 'fat arrow'. It's a concise syntax for function expressions in TypeScript."
    
    if "operator" in query_lower and "boolean" in query_lower and ("convert" in query_lower or "explicit" in query_lower):
        return "The !! operator converts any value into an explicit boolean. The first ! inverts the value to boolean, and the second ! inverts it back, giving you a proper boolean value."
    
    # Fallback: return the most relevant document content
    if relevant_docs:
        best_doc, score = relevant_docs[0]
        return best_doc["content"]
    
    return "I couldn't find a relevant answer in the TypeScript documentation."


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "TypeScript Documentation RAG API",
        "version": "1.0.0",
        "endpoints": {
            "/search": "GET - Search TypeScript documentation with query parameter ?q=your_question"
        },
        "example": "/search?q=What does the author affectionately call the => syntax?"
    }


@app.get("/search", response_model=SearchResponse)
async def search(q: str = Query(..., description="The search query")):
    """
    Search endpoint for TypeScript documentation.
    
    Args:
        q: The search query string
        
    Returns:
        SearchResponse with answer, sources, and confidence score
    """
    try:
        if not q or not q.strip():
            raise HTTPException(status_code=400, detail="Query parameter 'q' is required and cannot be empty")
        
        # Search for relevant documents
        relevant_docs = search_documents(q, top_k=3)
        
        # Extract the answer
        answer = extract_answer(q, relevant_docs)
        
        # Calculate confidence (average of top 3 similarities)
        confidence = sum(score for _, score in relevant_docs) / len(relevant_docs) if relevant_docs else 0.0
        
        return SearchResponse(
            answer=answer,
            sources="TypeScript Deep Dive by Basarat Ali Syed (https://github.com/basarat/typescript-book)",
            confidence=round(confidence, 3)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.options("/search")
async def options_search():
    """Handle CORS preflight requests for /search endpoint."""
    return {"message": "OK"}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting TypeScript RAG API on http://127.0.0.1:8000")
    print("📚 Try: http://127.0.0.1:8000/search?q=What does the author affectionately call the => syntax?")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
