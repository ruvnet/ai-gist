from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from app.models import GistCreateRequest, GistUpdateRequest, ChatRequest
from app.services import create_gist, update_gist, get_gist, list_gists
from app.lite_llm import chat_completion
import uvicorn
import httpx


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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
