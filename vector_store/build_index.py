import json
from embeddings.embedder import Embedder
from vector_store.chroma_store import ChromaStore

CHUNKS_PATH = "data/chunks/chunks.json"


def load_chunks():
    with open(CHUNKS_PATH, "r") as f:
        return json.load(f)


def main():
    chunks = load_chunks()

    texts = [chunk["content"] for chunk in chunks]

    print("Loading embedding model...")
    embedder = Embedder()

    print("Generating embeddings...")
    embeddings = embedder.embed_texts(texts)

    print("Storing in ChromaDB...")
    store = ChromaStore()
    store.add_documents(chunks, embeddings)

    print("Done! Vector DB ready.")


if __name__ == "__main__":
    import os

    print("Chroma DB path:", os.path.abspath("chroma_db"))
    main()