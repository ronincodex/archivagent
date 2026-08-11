# Archivagent 🗂️🤖

**Archivagent** is a lightweight, command-line interface (CLI) Retrieval-Augmented Generation (RAG) system designed to parse, vectorize, and query massive academic literature archives (such as the DBLP dataset) using ChromaDB.

---

## 🚀 Features
* **Stream-Based XML Parsing:** Efficiently processes massive compressed datasets (`.xml.gz`) without overwhelming system memory.
* **Vector Database Integration:** Embeds and indexes documents locally using **ChromaDB**.
* **Flexible Embedding Pipelines:** Supports both local CPU execution (via Ollama) and high-speed cloud integration (via OpenAI APIs).
* **CLI-First Workflow:** Fully optimized for terminal-based developers and server administrators.

---

## 🛠️ Project Structure
```text
archivagent/
├── src/
│   └── archivagent/
│       ├── agent/         # RAG query and interaction logic
│       ├── ingestion/     # XML stream parser and batch pipeline
│       └── vector_db/     # ChromaDB client configuration
├── .gitignore
└── README.md

📦 Quick Start
Step 1: Navigate to the repository
        Bash:
        cd archivagent
Step 2: Set up your environment and dependencies
        Bash:
        conda create -n archivagent python=3.13 -y
        conda activate archivagent
        pip install -r requirements.txt

Step 3: Run the ingestion pipeline
        Bash:
        python -m src.archivagent.ingestion.pipeline

---



