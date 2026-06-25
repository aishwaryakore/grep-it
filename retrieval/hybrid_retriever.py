import json

from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_classic.retrievers import EnsembleRetriever
# from langchain.retrievers import EnsembleRetriever

from embeddings.embedder import Embedder
from vector_store.chroma_store import ChromaStore
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
# from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

CHUNKS_PATH = "data/chunks/chunks.json"
RERANKER_MODEL = "rerank-english-v3.0"
RERANKER_TOP_N = 4          
RERANKER_SCORE_THRESHOLD = 0.5   

def load_chunk_documents():
    with open(CHUNKS_PATH, "r") as f:
        chunks = json.load(f)

    return [
        Document(
            page_content=chunk["content"],
            metadata={
                "source": chunk["source"],
                "section": chunk["section"],
                "title": chunk["title"]
            }
        )
        for chunk in chunks
    ]

def build_retriever(k=8):
    # Vector retriever
    store = ChromaStore()
    vector_retriever = store.as_retriever(search_kwargs={"k": k})

    # BM25 retriever
    documents = load_chunk_documents()
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = k

    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.5, 0.5]
    )

    compressor = CohereRerank(
        model=RERANKER_MODEL,
        top_n=RERANKER_TOP_N
    )

    reranking_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=hybrid_retriever
    )

    return reranking_retriever