import threading
import logging
from typing import List, Dict
from .models import get_last_three_chats, get_project, add_chat, add_summary, add_memory
from .prompts import summary_prompt, strands_prompt, generate_questions_prompt
from .memory.rag_utils import retrieve, upsert_strands
from .memory.llm_utils import LLMUtils 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def regenerate_summary(past_summary: str, new_facts: List[str], generate_response):
    try:
        logger.info("Regenerating summary")
        prompt = summary_prompt()
        user_prompt = f"""
        Here is the past summary: {past_summary}
        Here are the new facts: {new_facts}
        """

        summary = generate_response(prompt, user_prompt)
        logger.info("Summary regenerated successfully")
        return summary
    except Exception as e:
        logger.error(f"Failed to regenerate summary: {e}")
        raise

def generate_strands(chat_pair: Dict[str, str], generate_response):
    try:
        logger.info("Generating strands")
        prompt = strands_prompt()
        user_prompt = f"""
        Here is the chat pair: {chat_pair}
        """
        strands = generate_response(prompt, user_prompt, ast_parse_response=True)
        logger.info(f"Generated {len(strands) if strands else 0} strands successfully")
        return strands
    except Exception as e:
        logger.error(f"Failed to generate strands: {e}")
        raise

def generate_questions(chat_pair: Dict[str, str], generate_response):
    try:
        logger.info("Generating questions")
        prompt = generate_questions_prompt()
        user_prompt = f"""
        Here is the chat pair: {chat_pair}
        """
        questions = generate_response(prompt, user_prompt, ast_parse_response=True)
        logger.info(f"Generated {len(questions) if questions else 0} questions successfully")
        return questions
    except Exception as e:
        logger.error(f"Failed to generate questions: {e}")
        raise

def recall(api_key: str, project_name: str, chat_pair: Dict[str, str], openai_key: str):
    try:
        logger.info(f"Starting recall for project: {project_name}")
        llm = LLMUtils(api_key=openai_key)

        recent_chats_result = get_last_three_chats(api_key, project_name)
        if "error" in recent_chats_result:
            logger.warning(f"Could not retrieve recent chats: {recent_chats_result['error']}")
            recent_chats = []
        else:
            recent_chats = recent_chats_result.get("last_three_chats", [])
            logger.info("Recent chats retrieved successfully")

        project = get_project(api_key, project_name)
        if "error" in project:
            logger.error(f"Failed to retrieve project: {project['error']}")
            raise Exception(f"Project not found: {project['error']}")
        logger.info("Project retrieved successfully")

        summary = project.get("summaries", [])[-1]["summary"] if project.get("summaries") else ""
        logger.info("Summary retrieved successfully")

        questions = generate_questions(str(chat_pair), llm.get_response)
        logger.info("Questions generated successfully")

        ragged_memory = retrieve(questions, project_name, llm.embed)
        logger.info(f"Retrieved {len(ragged_memory)} memory items successfully")

        result = {
            "recent_chats": recent_chats,
            "summary": summary,
            "ragged_memory": ragged_memory
        }
        logger.info("Context package generated successfully")

        def background_update():
            try:
                logger.info("Starting background update")
                
                chat_result = add_chat(api_key, project_name, chat_pair["user"], chat_pair["assistant"])
                if "error" in chat_result:
                    logger.error(f"Failed to add chat: {chat_result['error']}")
                    return
                logger.info("Chat added successfully")
                
                strands = generate_strands(str(chat_pair), llm.get_response)
                logger.info("Strands generated successfully")
                
                for i, strand in enumerate(strands):
                    try:
                        memory_result = add_memory(api_key, project_name, strand)
                        if "error" in memory_result:
                            logger.warning(f"Failed to add memory strand {i+1}: {memory_result['error']}")
                            continue
                        logger.debug(f"Memory strand {i+1} added successfully")
                        
                        upsert_strands(strand, project_name, llm.embed)
                        logger.debug(f"Strand {i+1} upserted successfully")
                    except Exception as e:
                        logger.warning(f"Failed to process strand {i+1}: {e}")
                        continue
                
                updated_summary = regenerate_summary(summary, strands, llm.get_response)
                logger.info("Summary regenerated successfully")
                
                summary_result = add_summary(api_key, project_name, updated_summary)
                if "error" in summary_result:
                    logger.error(f"Failed to add summary: {summary_result['error']}")
                else:
                    logger.info("Summary added successfully")
                
                logger.info("Background update completed successfully")
            except Exception as e:
                logger.error(f"Error in background update: {e}")

        threading.Thread(target=background_update).start()
        logger.info("Background update thread started")
        logger.info("Recall completed successfully")
        return result
    except Exception as e:
        logger.error(f"Failed to complete recall for project {project_name}: {e}")
        raise