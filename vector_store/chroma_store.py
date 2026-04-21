import chromadb
from chromadb.config import Settings
import os

class ChromaStore:
    def __init__(self, collection_name="langchain_docs"):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        persist_path = os.path.join(BASE_DIR, "chroma_db")

        print("Chroma DB path:", persist_path)

        self.client = chromadb.PersistentClient(path=persist_path)

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(self, chunks, embeddings):
        ids = [f"id_{i}" for i in range(len(chunks))]

        documents = [chunk["content"] for chunk in chunks]

        metadatas = [
            {
                "source": chunk["source"],
                "section": chunk["section"],
                "title": chunk["title"]
            }
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

    def query(self, query_embedding, top_k=5):
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        return results