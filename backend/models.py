from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import uuid
import logging
import certifi
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

try:
    client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'), tls = True, tlsCAFile=certifi.where())
    db = client["reca11_db"]
    users_col = db["users"]
    projects_col = db["projects"]
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise


def validate_api_key(api_key):
    if not api_key or not isinstance(api_key, str):
        return False
    return api_key.startswith("rcll_") and len(api_key) == 41


def validate_project_name(project_name):
    if not project_name or not isinstance(project_name, str):
        return False
    if len(project_name) < 1 or len(project_name) > 100:
        return False
    return re.match(r'^[a-zA-Z0-9_-]+$', project_name)


def validate_content(content):
    if not content or not isinstance(content, str):
        return False
    return len(content.strip()) > 0 and len(content) <= 10000


def create_api_key():
    try:
        logger.info("Creating API key")
        api_key = "rcll_" + str(uuid.uuid4())
        user_doc = {
            "api_key": api_key,
            "created_at": datetime.now(),
            "projects": []
        }
        users_col.insert_one(user_doc)
        logger.info("API key created successfully")
        return api_key
    except Exception as e:
        logger.error(f"Failed to create API key: {e}")
        raise


def create_project(api_key, project_name):
    try:
        if not validate_api_key(api_key):
            logger.error("Invalid API key format")
            return {"error": "Invalid API key format"}
        
        if not validate_project_name(project_name):
            logger.error("Invalid project name")
            return {"error": "Invalid project name. Must be 1-100 chars, alphanumeric, underscore, or hyphen only"}
        
        logger.info(f"Creating project: {project_name} for user: {api_key}")
        existing = projects_col.find_one({"owner_api_key": api_key, "project_name": project_name})
        if existing:
            logger.warning(f"Project {project_name} already exists for user {api_key}")
            return {"error": "Project with this name already exists for this user."}

        project_doc = {
            "owner_api_key": api_key,
            "project_name": project_name,
            "created_at": datetime.now(),
            "memory_strands": [],
            "summaries": [{"summary": "", "timestamp": datetime.now()}],
            "chat_history": []
        }
        result = projects_col.insert_one(project_doc)
        users_col.update_one(
            {"api_key": api_key},
            {"$push": {"projects": result.inserted_id}}
        )
        logger.info("Project created successfully")
        return {"success": True, "project_id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Failed to create project {project_name}: {e}")
        raise


def add_memory(api_key, project_name, content):
    try:
        if not validate_api_key(api_key):
            logger.error("Invalid API key format")
            return {"error": "Invalid API key format"}
        
        if not validate_project_name(project_name):
            logger.error("Invalid project name")
            return {"error": "Invalid project name"}
        
        if not validate_content(content):
            logger.error("Invalid content")
            return {"error": "Content must be a non-empty string with max 10000 characters"}
        
        logger.info(f"Adding memory to project: {project_name}")
        memory_obj = {
            "content": content.strip(),
            "timestamp": datetime.now()
        }
        result = projects_col.update_one(
            {"owner_api_key": api_key, "project_name": project_name},
            {"$push": {"memory_strands": memory_obj}}
        )
        
        if result.matched_count == 0:
            logger.warning(f"Project {project_name} not found for user")
            return {"error": "Project not found"}
        
        logger.info("Memory added successfully")
        return {"modified_count": result.modified_count}
    except Exception as e:
        logger.error(f"Failed to add memory to project {project_name}: {e}")
        raise


def add_chat(api_key, project_name, user_msg, assistant_msg):
    try:
        if not validate_api_key(api_key):
            logger.error("Invalid API key format")
            return {"error": "Invalid API key format"}
        
        if not validate_project_name(project_name):
            logger.error("Invalid project name")
            return {"error": "Invalid project name"}
        
        if not validate_content(user_msg):
            logger.error("Invalid user message")
            return {"error": "User message must be a non-empty string with max 10000 characters"}
        
        if not validate_content(assistant_msg):
            logger.error("Invalid assistant message")
            return {"error": "Assistant message must be a non-empty string with max 10000 characters"}
        
        logger.info(f"Adding chat to project: {project_name}")
        chat_pair = {
            "user": user_msg.strip(),
            "assistant": assistant_msg.strip()
        }
        result = projects_col.update_one(
            {"owner_api_key": api_key, "project_name": project_name},
            {"$push": {"chat_history": chat_pair}}
        )
        
        if result.matched_count == 0:
            logger.warning(f"Project {project_name} not found for user")
            return {"error": "Project not found"}
        
        logger.info("Chat added successfully")
        return {"modified_count": result.modified_count}
    except Exception as e:
        logger.error(f"Failed to add chat to project {project_name}: {e}")
        raise


def add_summary(api_key, project_name, summary_text):
    try:
        if not validate_api_key(api_key):
            logger.error("Invalid API key format")
            return {"error": "Invalid API key format"}
        
        if not validate_project_name(project_name):
            logger.error("Invalid project name")
            return {"error": "Invalid project name"}
        
        if not validate_content(summary_text):
            logger.error("Invalid summary text")
            return {"error": "Summary text must be a non-empty string with max 10000 characters"}
        
        logger.info(f"Adding summary to project: {project_name}")
        summary_obj = {
            "timestamp": datetime.now(),
            "summary": summary_text.strip()
        }
        result = projects_col.update_one(
            {"owner_api_key": api_key, "project_name": project_name},
            {"$push": {"summaries": summary_obj}}
        )
        
        if result.matched_count == 0:
            logger.warning(f"Project {project_name} not found for user")
            return {"error": "Project not found"}
        
        logger.info("Summary added successfully")
        return {"modified_count": result.modified_count}
    except Exception as e:
        logger.error(f"Failed to add summary to project {project_name}: {e}")
        raise


def get_project(api_key, project_name):
    try:
        if not validate_api_key(api_key):
            logger.error("Invalid API key format")
            return {"error": "Invalid API key format"}
        
        if not validate_project_name(project_name):
            logger.error("Invalid project name")
            return {"error": "Invalid project name"}
        
        logger.info(f"Getting project: {project_name} for user: {api_key}")
        project = projects_col.find_one(
            {"owner_api_key": api_key, "project_name": project_name},
            {"_id": 0}
        )
        logger.info("Project retrieved successfully")
        return project or {"error": "Project not found."}
    except Exception as e:
        logger.error(f"Failed to get project {project_name}: {e}")
        raise

def get_last_three_chats(api_key, project_name):
    try:
        if not validate_api_key(api_key):
            logger.error("Invalid API key format")
            return {"error": "Invalid API key format"}
        
        if not validate_project_name(project_name):
            logger.error("Invalid project name")
            return {"error": "Invalid project name"}
        
        logger.info(f"Getting last 3 chats for project: {project_name} for user: {api_key}")
        project = projects_col.find_one(
            {"owner_api_key": api_key, "project_name": project_name},
            {"_id": 0, "chat_history": {"$slice": -3}}
        )
        if not project or "chat_history" not in project:
            logger.warning(f"Project {project_name} not found or no chat history")
            return {"error": "Project not found or no chat history."}
        
        logger.info("Last 3 chats retrieved successfully")
        return {"last_three_chats": project["chat_history"]}
    except Exception as e:
        logger.error(f"Failed to get last 3 chats for project {project_name}: {e}")
        raise