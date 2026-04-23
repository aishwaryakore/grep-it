# grep-it

**A context-aware developer knowledge assistant for LangChain — ask anything about LangChain and get accurate, doc-backed answers.**
 
grep-it is a RAG-powered assistant built specifically for the LangChain ecosystem. It ingests the official LangChain documentation, embeds it into a vector store, and lets developers query it in natural language — so you spend less time digging through docs and more time building.
 
---
 
## Features
 
- **LangChain docs, fully ingested** — Pre-loaded with content from the official LangChain documentation
- **Natural language Q&A** — Ask questions the way you'd ask a colleague: *"How do I use memory in a chain?"*
- **Context-aware retrieval** — Fetches the most semantically relevant doc sections to ground every answer
- **Semantic embeddings** — Meaning-aware vector search, not just keyword matching
- **Modular RAG pipeline** — Clean separation of ingestion, embedding, vector storage, and retrieval
- **Configurable** — Easily tune chunk sizes, embedding models, and retrieval settings via the config module
---
 
## Tech Stack
 
| Component | Technology |
|-----------|-----------|
| Language | Python |
| Knowledge source | LangChain Official Docs |
| Embeddings | OpenAI Embeddings |
| Vector Store | ChromaDB |
| LLM | OpenAI GPT |
| RAG framework | LangChain |
 
---
 
## Project Structure
 
```
grep-it/
├── config/          # Configuration: model names, chunk sizes, paths
├── embeddings/      # Embedding logic — converts text chunks to vectors
├── ingestion/       # LangChain docs loading and preprocessing
├── retrieval/       # Query handling and context-aware retrieval
├── vector_store/    # Vector store setup and management
├── main.py          # Entry point — runs the full pipeline
└── requirements.txt # Python dependencies
```
 
---
 