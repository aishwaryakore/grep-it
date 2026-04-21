import os
import json
from ingestion.chunking.chunker import create_chunks

INPUT_DIR = "data/cleaned"
OUTPUT_DIR = "data/chunks"


def load_documents():
    documents = []

    for file in os.listdir(INPUT_DIR):
        if file.endswith(".json"):
            path = os.path.join(INPUT_DIR, file)

            with open(path, "r") as f:
                doc = json.load(f)
                documents.append(doc)

    return documents


def save_chunks(chunks):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, "chunks.json")

    with open(output_path, "w") as f:
        json.dump(chunks, f, indent=2)

    print(f"Saved chunks to {output_path}")


def main():
    docs = load_documents()
    all_chunks = []

    for doc in docs:
        chunks = create_chunks(doc)
        all_chunks.extend(chunks)

    print(f"Total chunks created: {len(all_chunks)}")

    save_chunks(all_chunks)


if __name__ == "__main__":
    main()