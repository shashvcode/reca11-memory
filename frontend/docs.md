# Reca11 — Memory Layer for LLMs

**Reca11** is a plug-and-play memory layer for your LLM apps. It captures three key aspects of every conversation — recent history, core facts, and evolving themes — delivering a complete memory system through a simple API.

---

## Installation

```bash
pip install reca11


⸻

Generate an API Key

Visit https://reca11-memory.onrender.com
Click the “Generate API Key” button to instantly receive your key.

⸻

Quickstart

from reca11 import Reca11

rc = Reca11(
    api_key="your-api-key",
    openai_key="your-openai-key",
    project_name="my-project"
)

chat_pair = {
    "user": "What did I say I wanted to build?",
    "assistant": "You said you wanted to build a memory SDK for LLMs."
}

memory = rc.recall(chat_pair)

print(memory)


⸻

Health Check

To verify the backend is running, visit:

GET https://reca11-memory.onrender.com/health

Expected response:

{ "status": "ok" }


