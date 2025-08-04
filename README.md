# Reca11 — Memory Layer for LLMs

**Reca11** is a plug-and-play memory architecture designed to bring persistent, structured context to your LLM applications. It intelligently captures and stores three essential layers of conversational memory:

- **Recent chat history**
- **Standalone factual strands extracted from the dialogue**
- **Evolving thematic summaries that reflect the conversation’s trajectory over time**

The core reca11 function delivers a compact, high-relevance context package by combining all three elements. This ensures your LLM receives rich and persistent memory without overwhelming the context window.

I’m currently conducting a study that outlines this architecture in depth and benchmarks its performance against leading industry memory solutions.

Link to research article: COMING SOON!

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

Here’s how to get up and running in just a few lines:

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
