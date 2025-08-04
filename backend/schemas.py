from typing import Dict
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    api_key: str
    project_name: str

class MemoryStrandCreate(BaseModel):
    api_key: str
    project_name: str
    memory_strand: str

class ChatCreate(BaseModel):
    api_key: str
    project_name: str
    user_message: str
    assistant_message: str

class SummaryCreate(BaseModel):
    api_key: str
    project_name: str
    summary: str

class RecallRequest(BaseModel):
    api_key: str
    openai_key: str
    project_name: str
    chat_pair: Dict[str, str]


