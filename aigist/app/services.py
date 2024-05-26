import os
import httpx
import json
from typing import Dict, Optional, List
from .database import get_db
from .models import FileContent
from datetime import datetime

GITHUB_API_URL = "https://api.github.com/gists"
GITHUB_TOKEN = os.getenv("GH_TOKEN")

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

async def list_gists(page: int = 1, per_page: int = 30, since: Optional[str] = None, until: Optional[str] = None):
    params = {
        "page": page,
        "per_page": per_page
    }
    if since:
        params["since"] = since
    if until:
        params["until"] = until

    async with httpx.AsyncClient() as client:
        response = await client.get(
            GITHUB_API_URL,
            headers=headers,
            params=params
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
