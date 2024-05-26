import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import json
import os
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from app.models import GistCreateRequest, GistUpdateRequest, ChatRequest, ChatMessage
from app.services import create_gist, update_gist, get_gist, list_gists
from app.lite_llm import chat_completion
from litellm import completion 
import uvicorn
import httpx
import sqlite3
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

DATABASE_FILE = "./data/gists.db"
ENV_FILE = ".env"

def check_env_variables():
    # Check if GITHUB_TOKEN is set
    if not os.getenv("GITHUB_TOKEN"):
        raise RuntimeError("❌ GITHUB_TOKEN is not set. Please set it to proceed.")
    else:
        print("✅ GITHUB_TOKEN is set.")

    # Check if LITELLM_API_BASE is set
    if not os.getenv("LITELLM_API_BASE"):
        raise RuntimeError("❌ LITELLM_API_BASE is not set. Please set it to proceed.")
    else:
        print("✅ LITELLM_API_BASE is set.")

    # Check if LITELLM_API_KEY is set
    if not os.getenv("LITELLM_API_KEY"):
        raise RuntimeError("❌ LITELLM_API_KEY is not set. Please set it to proceed.")
    else:
        print("✅ LITELLM_API_KEY is set.")

    # Check if LITELLM_MODEL is set
    if not os.getenv("LITELLM_MODEL"):
        raise RuntimeError("❌ LITELLM_MODEL is not set. Please set it to proceed.")
    else:
        print("✅ LITELLM_MODEL is set.")

def set_env_variable(key, value):
    os.environ[key] = value
    with open(ENV_FILE, "a") as f:
        f.write(f"{key}={value}\n")

def prompt_user_for_env_vars():
    import readline  # Optional, will allow Up/Down/History in the prompt
    print("🔧 Some required environment variables are missing. Please enter them:")

    # Prompt for GITHUB_TOKEN
    if not os.getenv("GITHUB_TOKEN"):
        github_token = input("Enter GITHUB_TOKEN: ")
        set_env_variable("GITHUB_TOKEN", github_token)

    # Prompt for LITELLM_API_BASE
    if not os.getenv("LITELLM_API_BASE"):
        print("Select the LITELLM_API_BASE from the following options:")
        options = [
            "OpenAI (https://api.openai.com/v1)",
            "Microsoft Azure (https://api.cognitive.microsoft.com)",
            "Google Cloud (https://ai-platform.googleapis.com)",
            "IBM Watson (https://api.us-south.assistant.watson.cloud.ibm.com)",
            "Amazon AWS (https://runtime.sagemaker.amazonaws.com)",
            "Hugging Face (https://api-inference.huggingface.co)",
            "Cohere (https://api.cohere.ai)",
            "Anthropic (https://api.anthropic.com)",
            "AI21 Labs (https://api.ai21.com/studio/v1)",
            "AssemblyAI (https://api.assemblyai.com)",
            "Other"
        ]

        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = int(input("Enter the number of your choice: "))
        if choice in range(1, len(options) + 1):
            api_base = options[choice - 1].split(" ")[-1].strip("()")
        else:
            api_base = input("Enter LITELLM_API_BASE: ")
        set_env_variable("LITELLM_API_BASE", api_base)

    # Prompt for LITELLM_API_KEY
    if not os.getenv("LITELLM_API_KEY"):
        litellm_api_key = input("Enter LITELLM_API_KEY: ")
        set_env_variable("LITELLM_API_KEY", litellm_api_key)

    # Prompt for LITELLM_MODEL
    if not os.getenv("LITELLM_MODEL"):
        print("Enter the model for LITELLM (e.g., gpt-4o-2024-05-1):")
        litellm_model = input("Enter LITELLM_MODEL: ")
        set_env_variable("LITELLM_MODEL", litellm_model)

def check_db_and_table():
    # ASCII Art Header
    print(r"""
     _____ _ _____ _     _   
    |  _  |_|   __|_|___| |_ 
    |     | |  |  | |_ -|  _|
    |__|__|_|_____|_|___|_|  
                                          
        Created by rUv
    """)

    # Check and prompt for environment variables
    try:
        check_env_variables()
    except RuntimeError as e:
        print(e)
        prompt_user_for_env_vars()

    # Re-check the environment variables after prompting
    check_env_variables()

    # Check if sqlite3 is installed
    if not os.system("command -v sqlite3"):
        print("✅ SQLite3 is installed.")
    else:
        raise RuntimeError("❌ SQLite3 is not installed. Please install it to proceed.")

    # Check if the database file exists
    if not os.path.isfile(DATABASE_FILE):
        raise RuntimeError(f"❌ Database file '{DATABASE_FILE}' does not exist. Please create it to proceed.")
    else:
        print(f"✅ Database file '{DATABASE_FILE}' exists.")

    # Check if the 'gists' table exists
    print("🔍 Checking if the 'gists' table exists...")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gists';")
        table_exists = cursor.fetchone()
        if table_exists:
            print("✅ The 'gists' table exists.")
        else:
            raise RuntimeError("❌ The 'gists' table does not exist.")
    except sqlite3.Error as e:
        raise RuntimeError(f"❌ An error occurred: {e}")
    finally:
        if conn:
            conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    check_db_and_table()
    yield
    # Any cleanup can be done here
    print("🚀 AiGist Started")

app = FastAPI(lifespan=lifespan)

@app.post("/gists")
async def create_gist_endpoint(request: GistCreateRequest):
    files = {file.filename: {"content": file.content} for file in request.files}
    try:
        gist = await create_gist(request.description, request.public, files)
        return gist
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.patch("/gists/{gist_id}")
async def update_gist_endpoint(gist_id: str, request: GistUpdateRequest):
    files = {file.filename: {"content": file.content} for file in request.files}
    try:
        gist = await update_gist(gist_id, request.description, files)
        return gist
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    try:
        response = await chat_completion(chat_request.messages)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
@app.get("/gists")
async def list_gists_endpoint(
    page: int = Query(1, gt=0),
    per_page: int = Query(30, gt=0, le=100),
    since: Optional[str] = Query(None),
    until: Optional[str] = Query(None)
):
    try:
        gists = await list_gists(page, per_page, since, until)
        return gists
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


def main():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
