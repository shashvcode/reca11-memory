from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from .schemas import ProjectCreate, MemoryStrandCreate, ChatCreate, SummaryCreate, RecallRequest
from .models import (
    create_api_key, create_project, add_memory, add_chat, add_summary, 
    get_project, get_last_three_chats
)
from .utils import recall
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post("/project/create")
@limiter.limit("10/minute")
async def create_project_endpoint(request: Request, data: ProjectCreate):
    logger.info(f"Create project request for: {data.project_name}")
    result = create_project(data.api_key, data.project_name)
    if "error" in result:
        logger.error(f"Failed to create project {data.project_name}: {result['error']}")
        raise HTTPException(status_code=400, detail=result["error"])
    logger.info(f"Project {data.project_name} created successfully")
    return result

@router.post("/memory/add")
@limiter.limit("50/minute")
async def add_memory_endpoint(request: Request, data: MemoryStrandCreate):
    logger.info(f"Add memory request for project: {data.project_name}")
    result = add_memory(data.api_key, data.project_name, data.memory_strand)
    if result["modified_count"] == 0:
        logger.error(f"Failed to add memory to project {data.project_name}")
        raise HTTPException(status_code=404, detail="Project not found or memory not added")
    logger.info(f"Memory added to project {data.project_name}")
    return {"success": True, "message": "Memory strand added successfully"}

@router.post("/chat/add")
@limiter.limit("100/minute")
async def add_chat_endpoint(request: Request, data: ChatCreate):
    logger.info(f"Add chat request for project: {data.project_name}")
    result = add_chat(data.api_key, data.project_name, data.user_message, data.assistant_message)
    if result["modified_count"] == 0:
        logger.error(f"Failed to add chat to project {data.project_name}")
        raise HTTPException(status_code=404, detail="Project not found or chat not added")
    logger.info(f"Chat added to project {data.project_name}")
    return {"success": True, "message": "Chat pair added successfully"}

@router.post("/summary/add")
@limiter.limit("20/minute")
async def add_summary_endpoint(request: Request, data: SummaryCreate):
    logger.info(f"Add summary request for project: {data.project_name}")
    result = add_summary(data.api_key, data.project_name, data.summary)
    if result["modified_count"] == 0:
        logger.error(f"Failed to add summary to project {data.project_name}")
        raise HTTPException(status_code=404, detail="Project not found or summary not added")
    logger.info(f"Summary added to project {data.project_name}")
    return {"success": True, "message": "Summary added successfully"}

@router.get("/chat/recent")
@limiter.limit("30/minute")
async def get_recent_chats(request: Request, api_key: str, project_name: str):
    logger.info(f"Get recent chats request for project: {project_name}")
    result = get_last_three_chats(api_key, project_name)
    if "error" in result:
        logger.error(f"Failed to get recent chats for project {project_name}: {result['error']}")
        raise HTTPException(status_code=404, detail=result["error"])
    logger.info(f"Recent chats retrieved for project {project_name}")
    return result

@router.get("/project")
@limiter.limit("20/minute")
async def get_project_info(request: Request, api_key: str, project_name: str):
    logger.info(f"Get project info request for: {project_name}")
    result = get_project(api_key, project_name)
    if "error" in result:
        logger.error(f"Failed to get project {project_name}: {result['error']}")
        raise HTTPException(status_code=404, detail=result["error"])
    logger.info(f"Project info retrieved for {project_name}")
    return result

@router.post("/recall")
@limiter.limit("30/minute")
async def recall_memory(request: Request, data: RecallRequest):
    logger.info(f"Recall request for project: {data.project_name}")
    try:
        chat_pair = data.chat_pair
        result = recall(data.api_key, data.project_name, chat_pair, data.openai_key)
        logger.info(f"Recall completed for project {data.project_name}")
        return result
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in recall request for project {data.project_name}")
        raise HTTPException(status_code=400, detail="Invalid chat_pair JSON format")
    except Exception as e:
        logger.error(f"Error processing recall for project {data.project_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing recall: {str(e)}")

@router.post("/apikey/create")
@limiter.limit("5/minute")
async def create_api_key_endpoint(request: Request):
    logger.info("API key creation request")
    api_key = create_api_key()
    logger.info("API key created successfully")
    return {"api_key": api_key, "message": "API key created successfully"}

@router.get("/health")
@limiter.limit("60/minute")
async def health_check(request: Request):
    logger.info("Health check request")
    return {"status": "healthy", "service": "reca11-memory"}
