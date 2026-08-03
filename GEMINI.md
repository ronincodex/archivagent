# Project Context: archivagent
You are an AI engineering coding assistant helping build an enterprise RAG Application.

## Tech Stack & Environment
**Python Version:** 3.13 (Conda environment: archivagent)
**Frameworks:** FastAPI, Uvicorn, Pydantic, Google Antigravity
**Local LLM:** Ollama (running qwen2.5:1.5b via CPU-only at http://127.0.0.1:11434)

## Conding Standards
**Formatting:** All python code must strictly adhere to Black and isort formatting rules.
**typing:** Use strict Python type hints.
**Constraints:** Do not use GPU-specific optimizations. The host machine operates strictly on an Intel Haswell CPU using AVX2 instructions without Vulkan support. Code must be CPU bound.
