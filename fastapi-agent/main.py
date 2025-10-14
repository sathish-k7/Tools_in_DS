import os
import subprocess
import tempfile
import shutil
import logging
from datetime import datetime
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent_runs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="CLI Coding Agent Delegator")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CLI Coding Agent API",
        "endpoints": {
            "/task": "GET /task?q=<task_description>"
        }
    }

@app.get("/task")
async def execute_task(q: str = Query(..., description="Task description for the coding agent")):
    """
    Execute a task using a CLI coding agent.
    
    Args:
        q: Task description to be executed by the agent
        
    Returns:
        JSON with task, agent, output, and email
    """
    logger.info(f"Received task: {q}")
    
    # Create a temporary directory for the agent to work in
    temp_dir = tempfile.mkdtemp(prefix="agent_task_")
    logger.info(f"Created temporary workspace: {temp_dir}")
    
    try:
        # Prepare the command for GitHub Copilot CLI
        # Using --allow-all-tools to let the agent create files and run code
        cmd = [
            "copilot",
            "--allow-all-tools",
            "-p",
            q
        ]
        
        logger.info(f"Executing command: {' '.join(cmd)}")
        logger.info(f"Working directory: {temp_dir}")
        
        # Execute the command
        result = subprocess.run(
            cmd,
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        # Combine stdout and stderr for complete output
        output = result.stdout
        if result.stderr:
            output += f"\n{result.stderr}"
        
        # Log the result
        logger.info(f"Agent exit code: {result.returncode}")
        logger.info(f"Agent output length: {len(output)} chars")
        logger.info(f"Raw output: {output[:500]}")
        
        # Clean the output - extract just the final answer if possible
        cleaned_output = output.strip()
        
        # Try to extract just the meaningful answer
        lines = cleaned_output.split('\n')
        
        # Remove usage statistics and metadata lines
        filtered_lines = []
        skip_patterns = ['Total usage', 'Total duration', 'Usage by model', 'cache', 'Premium request', 'lines added', 'lines removed']
        
        for line in lines:
            # Skip lines with usage statistics
            if any(pattern in line for pattern in skip_patterns):
                continue
            # Skip empty lines
            if not line.strip():
                continue
            # Skip lines that are just bullets
            if line.strip() in ['●', '•', '-', '*']:
                continue
            filtered_lines.append(line.strip())
        
        # For Fibonacci or numeric tasks, try to extract just the number
        for line in reversed(filtered_lines):
            line = line.strip('● •-*').strip()
            # Check if line contains a number (possibly with explanation)
            if line.isdigit():
                cleaned_output = line
                break
            # Try to extract number from sentences like "The answer is 2584"
            import re
            numbers = re.findall(r'\b\d+\b', line)
            if numbers:
                # If task mentions Fibonacci and we found a number, use it
                if 'fibonacci' in q.lower() or 'print' in q.lower():
                    # Get the last (usually largest) number found
                    cleaned_output = numbers[-1]
                    break
        
        # If we still have the full output, join filtered lines
        if cleaned_output == output.strip() and filtered_lines:
            cleaned_output = '\n'.join(filtered_lines)
        
        response_data = {
            "task": q,
            "agent": "copilot-cli",
            "output": cleaned_output,
            "email": "24f1000011@ds.study.iitm.ac.in"
        }
        
        logger.info(f"Response: {response_data}")
        
        return JSONResponse(content=response_data)
        
    except subprocess.TimeoutExpired:
        logger.error("Agent execution timed out")
        return JSONResponse(
            content={
                "task": q,
                "agent": "copilot-cli",
                "output": "Error: Task execution timed out",
                "email": "24f1000011@ds.study.iitm.ac.in"
            },
            status_code=408
        )
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}", exc_info=True)
        return JSONResponse(
            content={
                "task": q,
                "agent": "copilot-cli",
                "output": f"Error: {str(e)}",
                "email": "24f1000011@ds.study.iitm.ac.in"
            },
            status_code=500
        )
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temporary workspace: {temp_dir}")
        except Exception as e:
            logger.warning(f"Failed to clean up temp directory: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
