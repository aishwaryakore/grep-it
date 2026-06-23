from ingestion.run_ingestion import run_ingestion
from ingestion.chunking.run_chunking import main as run_chunking
from vector_store.build_index import main as build_index

print("=== Step 1: Ingestion ===")
run_ingestion()

print("\n=== Step 2: Chunking ===")
run_chunking()

print("\n=== Step 3: Building Vector Index ===")
build_index()

print("\nPipeline complete.")