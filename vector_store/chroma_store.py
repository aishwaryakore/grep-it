import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from embeddings.embedder import Embedder
from typing import List

class ChromaStore:
    def __init__(self, collection_name: str = "langchain_docs"):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        persist_path = os.path.join(BASE_DIR, "chroma_db")

        print("Chroma DB path:", persist_path)

        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=Embedder(),
            persist_directory=persist_path
        )

    def add_documents(self, chunks: List[dict]):
        documents = [
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

        self.vectorstore.add_documents(documents)

    def as_retriever(self, **kwargs):
        return self.vectorstore.as_retriever(**kwargs)