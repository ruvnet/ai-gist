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
    files: List[GistFile]

class GistUpdateRequest(BaseModel):
    description: Optional[str]
    files: List[GistFile]

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    stream: bool = False

class GistFilterRequest(BaseModel):
    since: Optional[str] = None
    per_page: Optional[int] = 30
    page: Optional[int] = 1
