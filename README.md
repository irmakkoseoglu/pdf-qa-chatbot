---
title: PDF QA Chatbot
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# PDF QA Chatbot

RAG-based PDF question answering API built with FastAPI, LangChain, ChromaDB, and HuggingFace.

## Stack
- FastAPI
- LangChain
- ChromaDB
- HuggingFace Embeddings (all-MiniLM-L6-v2)
- Mistral-7B-Instruct (HuggingFace Inference API)

## Note on LLM
Default model is Mistral-7B via HuggingFace Inference API.
For better/different results, change `LLM_MODEL` in `main_deploy.py`.

## Endpoints
- `POST /upload` — PDF yükle
- `POST /query` — Soru sor
- `GET /` — Sağlık kontrolü
