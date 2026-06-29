---
title: PDF QA Chatbot
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# PDF Question Answering API

A RAG-based (Retrieval-Augmented Generation) REST API that allows users to upload PDF documents and ask questions about their content using semantic search and large language models.

## Live Demo
API Docs: https://irmakkoseoglu-pdf-qa-chatbot.hf.space/docs

## Tech Stack
- **FastAPI** — REST API framework
- **LangChain** — RAG pipeline orchestration
- **ChromaDB** — Vector database for semantic search
- **HuggingFace Embeddings** — `sentence-transformers/all-MiniLM-L6-v2`
- **Mistral-7B-Instruct** — LLM for answer generation (via HuggingFace Inference API)
- **Docker** — Containerization

## Project Structure
QA_chatbot/
├── main.py              # Local version (Ollama + TinyLlama)
├── main_deployed.py     # Deploy version (HuggingFace Inference API)
├── Dockerfile
├── requirements.txt
└── README.md

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/upload` | Upload a PDF file |
| POST | `/query` | Ask a question about uploaded PDFs |

## Deployment
Deployed on HuggingFace Spaces using Docker.
The `Dockerfile` defines the container environment — installs dependencies from `requirements.txt` and starts the FastAPI server on port 7860.

## Local Development
```bash
# Install Ollama and pull model
ollama pull tinyllama

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload
```

## Note on LLM
- **Local:** TinyLlama via Ollama (`main.py`)
- **Deployed:** Mistral-7B-Instruct via HuggingFace Inference API (`main_deployed.py`)
