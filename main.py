from retrieval.rag_pipeline import RAGPipeline

rag = RAGPipeline()

query = input("Ask a question about LangChain: ")

answer, sources, _ = rag.query(query)

print("\nAnswer:\n")
print(answer)

print("\nSources:")
for url in sources:
    print(f"- {url}")