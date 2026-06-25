# grep-it 🔍

**A context-aware developer knowledge assistant for LangChain — ask anything and get accurate, doc-grounded answers.**

grep-it is a production-style RAG pipeline built on LangChain's official documentation. It combines hybrid retrieval, reranking, query rewriting, and conversation memory to deliver precise, grounded answers to developer questions — with a clean Streamlit chat interface.

---

## Demo

> **User:** How do I add tools to an agent in LangChain?
>
> **grep-it:** To add tools to a LangChain agent, you pass them directly to `create_agent()`...
> *(with clickable source links to the official docs)*

---

## Architecture

```
User Query
     │
     ▼
Query Rewriter (GPT-4o-mini)
     │  rewrites vague queries into precise technical language
     ▼
Hybrid Retriever
  ├── BM25 (keyword search)
  └── ChromaDB (semantic search, MiniLM embeddings)
     │  EnsembleRetriever merges results
     ▼
Cohere Reranker
     │  scores each (query, chunk) pair, keeps top 4
     ▼
GPT-4o-mini
     │  grounded generation — uses only retrieved context
     ▼
Answer + Source URLs
```

---

## Features

- **Hybrid retrieval** — combines BM25 keyword search and semantic vector search via `EnsembleRetriever` for better coverage than either alone
- **Cohere reranking** — cross-encoder reranking filters noisy retrieval results before generation
- **Query rewriting** — vague or conversational questions are rewritten into precise technical queries before retrieval
- **Conversation memory** — retains the last 2 exchanges so follow-up questions resolve correctly
- **Grounded generation** — strict prompt instructs the LLM to answer only from retrieved context, not training knowledge
- **Custom ingestion pipeline** — scrapes, cleans, and chunks LangChain docs with heading-aware, code-block-safe chunking
- **RAGAS evaluation** — quantitative retrieval and generation quality scores on a curated test set
- **Streamlit chat UI** — clean conversational interface with clickable source links

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | LangChain |
| LLM | GPT-4o-mini (OpenAI) |
| Embeddings | all-MiniLM-L6-v2 (local, sentence-transformers) |
| Vector Store | ChromaDB |
| Retrieval | BM25 + ChromaDB via EnsembleRetriever |
| Reranking | Cohere rerank-english-v3.0 |
| Evaluation | RAGAS |
| UI | Streamlit |

---

## Project Structure

```
grep-it/
├── app.py                        # Streamlit chat UI
├── main.py                       # CLI entry point for querying
├── run_pipeline.py               # Runs ingestion → chunking → indexing
├── config/
│   └── settings.py               # ALLOWED_PATHS, base URL, output dirs
├── ingestion/
│   ├── run_ingestion.py          # Orchestrates scraping + cleaning
│   ├── loaders/
│   │   └── web_loader.py         # Fetches raw HTML from URLs
│   ├── cleaners/
│   │   └── html_cleaner.py       # Extracts structured text from HTML
│   ├── chunking/
│   │   ├── chunker.py            # Heading-aware, code-block-safe chunking
│   │   └── run_chunking.py       # Runs chunker over cleaned docs
│   └── utils/
│       ├── url_collector.py      # Collects URLs from sitemap
│       ├── parser.py             # Extracts page title
│       └── saver.py              # Saves docs to disk
├── embeddings/
│   └── embedder.py               # Local MiniLM embeddings
├── vector_store/
│   ├── chroma_store.py           # ChromaDB wrapper
│   └── build_index.py            # Embeds chunks and builds the index
├── retrieval/
│   ├── hybrid_retriever.py       # BM25 + vector + Cohere reranking
│   ├── query_rewriter.py         # Rewrites queries before retrieval
│   ├── rag_pipeline.py           # Full RAG pipeline with memory
│   └── prompts.py                # RAG and rewrite prompt templates
├── evals/
│   ├── evaluate.py               # RAGAS evaluation script
│   ├── test_dataset.json         # 8 hand-written Q&A pairs
│   └── results/
│       └── scores.json           # Latest RAGAS scores
└── data/
    ├── raw/                      # Raw scraped HTML docs
    ├── cleaned/                  # Cleaned markdown-style text
    └── chunks/                   # Final chunks ready for embedding
```

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/yourusername/grep-it.git
cd grep-it
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
HF_TOKEN=your_huggingface_token  # optional, suppresses rate limit warnings
```

### 3. Run the ingestion pipeline

```bash
python3 run_pipeline.py
```

This scrapes LangChain docs → cleans HTML → chunks content → builds the ChromaDB index.

### 4. Run the app

```bash
streamlit run app.py
```

Or use the CLI:

```bash
python3 main.py
```

---

## Run Evaluation

```bash
python3 -m evals.evaluate
```

Results are saved to `evals/results/scores.json`.

---

## How the Ingestion Pipeline Works

1. **URL collection** — reads `docs.langchain.com/sitemap.xml` and filters to `ALLOWED_PATHS` in `config/settings.py`
2. **Scraping** — fetches each page and saves raw HTML
3. **Cleaning** — extracts headings, paragraphs, bullet points, and code blocks; strips nav/sidebar/footer
4. **Chunking** — splits by heading sections first, then by word count (500 words, 100 overlap); never splits inside a code block so explanations and their code examples stay together
5. **Embedding** — encodes each chunk with local MiniLM model
6. **Indexing** — stores vectors in ChromaDB with source URL and section metadata

---

## Challenges & Design Decisions

- **Code-block-safe chunking** — standard word-count chunkers split mid-code, separating explanations from their examples. The chunker detects ` ``` ` boundaries and treats code blocks as atomic units.
- **Hybrid retrieval over pure semantic search** — technical identifiers like `create_agent` or `RunnableLambda` retrieve better with exact keyword matching (BM25) than embeddings alone.
- **Query rewriting before retrieval** — developer questions are often vague ("how does memory work?"). Rewriting them to precise technical language ("LangChain short-term memory management in agent loop") significantly improves retrieval recall.
- **Grounded prompt design** — the LLM is explicitly instructed not to use training knowledge, only retrieved context. This trades completeness for factual accuracy, which is the right tradeoff for a documentation assistant.