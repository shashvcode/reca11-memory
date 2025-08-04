from pinecone import Pinecone
from dotenv import load_dotenv
import os
import uuid
import logging
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

try:
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(host=os.getenv("PINECONE_HOST"))
    logger.info("Successfully initialized Pinecone connection")
except Exception as e:
    logger.error(f"Failed to initialize Pinecone: {e}")
    raise

def upsert_strands(strand: str, project_name: str, embed):
    try:
        logger.info(f"Starting upsert for project: {project_name}")
        embedding = embed(strand)
        strand_id = f"{project_name}_{str(uuid.uuid4())}"

        index.upsert(
            vectors=[
                {
                    "id": strand_id,
                    "values": embedding,
                    "metadata": {
                        "project_name": project_name,
                        "fact_text": strand  
                    }
                }
            ],
            namespace=project_name  
        )
        logger.info(f"Successfully upserted strand with ID: {strand_id}")
        return strand_id
    except Exception as e:
        logger.error(f"Failed to upsert strand for project {project_name}: {e}")
        raise

def retrieve(questions: List[str], project_name: str, embed):
    try:
        logger.info(f"Starting retrieval for project: {project_name} with {len(questions)} questions")
        retrieved_facts = []

        for i, question in enumerate(questions):
            try:
                logger.debug(f"Processing question {i+1}/{len(questions)}")
                embedding = embed(question)
                result = index.query(
                    vector=embedding,
                    top_k=2,
                    namespace=project_name,
                    include_metadata=True
                )
                
                matches_count = len(result.get("matches", []))
                logger.debug(f"Found {matches_count} matches for question {i+1}")
                
                for match in result.get("matches", []):
                    fact = match.get("metadata", {}).get("fact_text")
                    if fact:
                        retrieved_facts.append(fact)
            except Exception as e:
                logger.warning(f"Failed to process question {i+1}: {e}")
                continue

        unique_facts = list(set(retrieved_facts))
        logger.info(f"Retrieved {len(unique_facts)} unique facts from {len(retrieved_facts)} total matches")
        return unique_facts
    except Exception as e:
        logger.error(f"Failed to retrieve facts for project {project_name}: {e}")
        raise