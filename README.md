# Reca11 — Memory Layer for LLMs

**Reca11** is a plug-and-play memory architecture designed to add persistent context to your LLM applications. It intelligently tracks and stores three core components of every conversation:

- **Recent chat history**
- **Core user facts**
- **Evolving thematic summaries**

This enables better recall, continuity, and personalization in any app powered by large language models.
Link to research article : COMING SOON!

---

## Installation

Install the SDK via pip:

```bash
pip install reca11-core


⸻

Generate an API Key

To use the memory service, you’ll need an API key.

Visit:
https://reca11-memory-1.onrender.com
Click the “Generate API Key” button to instantly receive a unique key.

⸻

Quickstart

Here’s how to get up and running in just a few lines:

from recall_core import Reca11

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

To verify the backend is online:

GET https://reca11-memory.onrender.com/health

Expected response:

{ "status": "ok" }


⸻

License

This project is open-sourced under the terms of the MIT License.

---
