import json
from vector_store.chroma_store import ChromaStore

CHUNKS_PATH = "data/chunks/chunks.json"

def load_chunks():
    with open(CHUNKS_PATH, "r") as f:
        return json.load(f)

def main():
    chunks = load_chunks()

    print("Initializing store and embedding model...")
    store = ChromaStore()

    print("Generating embeddings and storing in ChromaDB...")
    store.add_documents(chunks)

    print("Done! Vector DB ready.")

if __name__ == "__main__":
    main()