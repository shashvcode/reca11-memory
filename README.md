# Reca11 — Memory Layer for LLMs

**Reca11** is a plug-and-play memory architecture designed to bring persistent, structured context to your LLM applications through intelligent retrieval-augmented generation (RAG) and advanced deduplication systems.

While LLMs are becoming more cohesive and capable by the day, they're often of no use if they can't remember what happened before. Without memory, every conversation starts from scratch, forcing users to repeat themselves and losing valuable context. The reca11 SDK was built to solve this fundamental limitation with a multi-layered approach.

## How Reca11 Works

Reca11 intelligently captures and stores three essential layers of conversational memory:

### 1. **Recent Chat History**
Maintains the most recent conversation turns with immediate persistence, ensuring that context retrieval always includes the latest interactions without timing delays.

### 2. **Semantic Memory Strands** 
Extracts standalone factual information from dialogues and stores them as embedding vectors in a Pinecone vector database. Each strand undergoes smart deduplication using:
- **Semantic similarity matching**: Retrieves the top-3 most similar existing strands using vector embeddings
- **AI duplicate detection**: Uses language models to determine if new information is truly novel or redundant
- **Intelligent filtering**: Only stores genuinely new factual content, preventing memory bloat and redundancy
- **Timestamping**: Maintains a temporal thread that chronologically categorizes memories, proving particularly useful when dealing with evolving factual strands

### 3. **Dynamic Thematic Summaries**
Maintains evolving summaries that capture the entire conversation's trajectory and key themes over time, automatically updating as new information becomes available.

This multi-layered approach ensures your LLM receives rich, persistent memory that grows smarter over time while maintaining efficiency and avoiding information redundancy.


---

## Installation

Install the SDK via pip:

```bash
pip install reca11-memory
```

---

## Generate an API Key

To use the memory service, you’ll need an API key.

Visit: [https://reca11-memory-1.onrender.com](https://reca11-memory-1.onrender.com)  
Click the **"Generate API Key"** button to instantly receive a unique key.

---

## Quickstart

Here’s how to get up and running in just a few lines. 

```python
from reca11 import Reca11

rc = Reca11(
    api_key="your-api-key",
    openai_key="your-openai-key",
    project_name="my-project"
)

chat_pair = {
    "assistant": "Hi! What did you do today?",
    "user": "I tried pineapple on pizza. Safe to say I'm not a fan!"
}

memory = rc.recall(chat_pair)

print(memory)
```
The final output of this code snippet is a memory context package that can be directly fed into the system prompt of an LLM:

---

## Retrieving Memory Strands

To access all stored memory strands for your project:

```python
# Get all memory strands
strands = rc.get_strands()

print(strands)
```

This returns all factual memory strands that have been extracted and stored from your conversations, including their content and timestamps:

```json
{
  "memory_strands": [
    {
      "content": "User doesn't like pineapple on pizza",
      "timestamp": "2023-12-01T10:30:00"
    },
    {
      "content": "User tried a new food combination today",
      "timestamp": "2023-12-01T10:30:00"
    }
  ]
}
```

---

## Health Check

To verify the backend is online:

```
GET https://reca11-memory.onrender.com/health
```

**Expected response:**

```json
{ "status": "ok" }
```

---

## License

This project is open-sourced under the terms of the MIT License.
