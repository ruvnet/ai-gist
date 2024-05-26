#!/bin/bash

# Create directory structure
mkdir -p project_root/.devcontainer
mkdir -p project_root/app
mkdir -p project_root/data
mkdir -p project_root/scripts
mkdir -p project_root/tests

# Create and populate .devcontainer/devcontainer.json
cat <<EOL > project_root/.devcontainer/devcontainer.json
{
  "name": "Python FastAPI",
  "image": "mcr.microsoft.com/vscode/devcontainers/python:3.9",
  "postCreateCommand": "bash .devcontainer/setup.sh"
}
EOL

# Create and populate .devcontainer/setup.sh
cat <<EOL > project_root/.devcontainer/setup.sh
#!/bin/bash

set -e

echo "Setting up the development environment..."

# Install dependencies
pip install -r requirements.txt

# Set up SQLite database
if [ ! -f data/gists.db ]; then
  echo "Creating SQLite database..."
  sqlite3 data/gists.db < .devcontainer/schema.sql
fi

# Menu for additional setup options
while true; do
  echo "Choose an option:"
  echo "1. Install additional packages"
  echo "2. Configure environment variables"
  echo "3. Optimize environment"
  echo "4. Exit"
  read -p "Enter your choice [1-4]: " choice
  case \$choice in
    1)
      read -p "Enter package name: " package
      pip install \$package
      ;;
    2)
      read -p "Enter environment variable name: " var_name
      read -p "Enter environment variable value: " var_value
      export \$var_name=\$var_value
      echo "export \$var_name=\$var_value" >> ~/.bashrc
      ;;
    3)
      echo "Optimizing environment..."
      # Add optimization commands here
      ;;
    4)
      break
      ;;
    *)
      echo "Invalid choice!"
      ;;
  esac
done

echo "Setup complete!"
EOL

# Create and populate .devcontainer/schema.sql
cat <<EOL > project_root/.devcontainer/schema.sql
CREATE TABLE IF NOT EXISTS gists (
    id TEXT PRIMARY KEY,
    description TEXT,
    public BOOLEAN,
    files TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
EOL

# Create and populate app/__init__.py
touch project_root/app/__init__.py

# Create and populate app/main.py
cat <<EOL > project_root/app/main.py
from fastapi import FastAPI, HTTPException, Depends
from .models import GistCreateRequest, GistUpdateRequest, ChatRequest
from .services import create_gist, update_gist, get_gist
from .lite_llm import chat_completion

app = FastAPI()

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

@app.post("/chat/gist")
async def chat_gist_endpoint(chat_request: ChatRequest):
    try:
        response = await chat_completion(chat_request.messages)
        action = response.get("action")
        if action == "create_gist":
            gist_data = response.get("gist_data")
            gist = await create_gist(gist_data["description"], gist_data["public"], gist_data["files"])
            return gist
        elif action == "update_gist":
            gist_id = response.get("gist_id")
            gist_data = response.get("gist_data")
            existing_gist = await get_gist(gist_id)
            updated_files = {**existing_gist["files"], **gist_data["files"]}
            gist = await update_gist(gist_id, gist_data.get("description", existing_gist["description"]), updated_files)
            return gist
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
EOL

# Create and populate app/models.py
cat <<EOL > project_root/app/models.py
from pydantic import BaseModel
from typing import List, Dict, Optional

class FileContent(BaseModel):
    content: str

class GistFile(BaseModel):
    filename: str
    content: str

class GistCreateRequest(BaseModel):
    description: str
    public: bool
    files: List<GistFile]

class GistUpdateRequest(BaseModel):
    description: Optional[str]
    files: List[GistFile]

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    stream: bool = False
EOL

# Create and populate app/services.py
cat <<EOL > project_root/app/services.py
import os
import httpx
import json
from .database import get_db

GITHUB_API_URL = "https://api.github.com/gists"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

async def create_gist(description: str, public: bool, files: Dict[str, FileContent]):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_API_URL,
            headers=headers,
            json={"description": description, "public": public, "files": files}
        )
        response.raise_for_status()
        gist = response.json()
        save_gist_to_db(gist)
        return gist

async def update_gist(gist_id: str, description: Optional[str], files: Dict[str, FileContent]):
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{GITHUB_API_URL}/{gist_id}",
            headers=headers,
            json={"description": description, "files": files}
        )
        response.raise_for_status()
        gist = response.json()
        save_gist_to_db(gist)
        return gist

async def get_gist(gist_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_URL}/{gist_id}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()

def save_gist_to_db(gist):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO gists (id, description, public, files, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (gist["id"], gist["description"], gist["public"], json.dumps(gist["files"]), gist["created_at"], gist["updated_at"])
        )
        conn.commit()
EOL

# Create and populate app/database.py
cat <<EOL > project_root/app/database.py
import sqlite3
from contextlib import contextmanager

DATABASE = "data/gists.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()
EOL

# Create and populate app/lite_llm.py
cat <<EOL > project_root/app/lite_llm.py
import os
from lite_llm import completion

async def chat_completion(messages):
    response = await completion(
        model="gpt-4o",
        messages=messages,
        api_base=os.getenv("LITELLM_API_BASE"),
        api_key=os.getenv("LITELLM_API_KEY"),
        stream=False
    )
    return response
EOL

# Create and populate scripts/create_folders.sh
cat <<EOL > project_root/scripts/create_folders.sh
#!/bin/bash

echo "Enter the name for the new directory:"
read NEW_DIR

if [ ! -d "\$NEW_DIR" ]; then
  mkdir -p "\$NEW_DIR"
  echo "Directory \$NEW_DIR created."
else
  echo "Directory \$NEW_DIR already exists."
fi

echo "Enter the names of the files to create (space-separated):"
read FILE_NAMES

for FILE in \$FILE_NAMES; do
  touch "\$NEW_DIR/\$FILE"
  echo "File \$FILE created in \$NEW_DIR."
done
EOL

# Create and populate tests/test_main.py
cat <<EOL > project_root/tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_gist():
    response = client.post("/gists", json={
        "description": "Test Gist",
        "public": True,
        "files": [{"filename": "test.txt", "content": "Hello World"}]
    })
    assert response.status_code == 200
    assert response.json()["description"] == "Test Gist"

def test_update_gist():
    gist_id = "existing_gist_id"
    response = client.patch(f"/gists/{gist_id}", json={
        "description": "Updated Gist",
        "files": [{"filename": "test.txt", "content": "Updated Content"}]
    })
    assert response.status_code == 200
    assert response.json()["description"] == "Updated Gist"
EOL

# Create and populate tests/test_services.py
cat <<EOL > project_root/tests/test_services.py
import pytest
from app.services import create_gist, update_gist

@pytest.mark.asyncio
async def test_create_gist():
    gist = await create_gist("Test Gist", True, {"test.txt": {"content": "Hello World"}})
    assert gist["description"] == "Test Gist"

@pytest.mark.asyncio
async def test_update_gist():
    gist_id = "existing_gist_id"
    gist = await update_gist(gist_id, "Updated Gist", {"test.txt": {"content": "Updated Content"}})
    assert gist["description"] == "Updated Gist"
EOL

# Create and populate .gitignore
cat <<EOL > project_root/.gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
EOL

# Create and populate README.md
cat <<EOL > project_root/README.md
# FastAPI Gist Manager

This project provides a FastAPI application to create and update GitHub gists using the GitHub API. It includes SQLite for persistence and is designed to run in a GitHub Codespace.

## Setup

1. **Create a GitHub Codespace**:
   - Create a new GitHub Codespace for your repository.
   - Ensure your GitHub token is stored as a secret in the Codespace.

2. **Install Dependencies**:
   - The setup script will automatically install necessary dependencies and set up the environment.

3. **Run the Application**:
   - Start the FastAPI server using Uvicorn:
     \`\`\`bash
     uvicorn app.main:app --reload
     \`\`\`

## Endpoints

- **Create Gist**: \`POST /gists\`
- **Update Gist**: \`PATCH /gists/{gist_id}\`
- **Chat Completion**: \`POST /chat\`
- **Chat Gist**: \`POST /chat/gist\`

## Testing

Run the tests using pytest:
\`\`\`bash
pytest
\`\`\`
EOL

# Create and populate requirements.txt
cat <<EOL > project_root/requirements.txt
fastapi
uvicorn
pydantic
httpx
sqlite3
lite-llm
EOL

# Create persistence.json
touch project_root/persistence.json

echo "Project structure created successfully."
