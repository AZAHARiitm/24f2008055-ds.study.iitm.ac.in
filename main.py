import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import tempfile
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/task")
async def run_task(q: str):
    logger.info(f"Received task: {q}")

    try:
        # Create a temporary directory for the agent to work in
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a prompt file
            prompt_file = os.path.join(temp_dir, "prompt")
            with open(prompt_file, "w") as f:
                f.write(q)

            # Run the gpt-engineer CLI tool
            process = subprocess.run(
                [
                    "gpt-engineer",
                    "--steps",
                    "simple_gen",
                    temp_dir,
                    "--prompt_file",
                    prompt_file,
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            # Log the output from the agent
            logger.info(f"Agent output: {process.stdout}")
            logger.error(f"Agent error (if any): {process.stderr}")

            # Find the output file
            output_file = os.path.join(temp_dir, "workspace", "all_output.txt")
            if not os.path.exists(output_file):
                raise HTTPException(status_code=500, detail="Output file not found")

            with open(output_file, "r") as f:
                output_content = f.read()

        # Format the response
        response = {
            "task": q,
            "agent": "gpt-engineer",
            "output": output_content,
            "email": "24f2008055@ds.study.iitm.ac.in",
        }
        return response

    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while running the agent: {e}")
        logger.error(f"Agent stdout: {e.stdout}")
        logger.error(f"Agent stderr: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"An error occurred while running the agent: {e.stderr}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
