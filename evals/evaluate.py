import os
import json
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from retrieval.rag_pipeline import RAGPipeline

DATASET_PATH = "evals/test_dataset.json"
RESULTS_PATH = "evals/results/scores.json"

def load_dataset():
    with open(DATASET_PATH, "r") as f:
        return json.load(f)
    
def run_pipeline_on_dataset(pipeline, dataset):
    """Run our RAG pipeline on every question in the test set."""
    results = []

    for i, item in enumerate(dataset):
        question = item["question"]
        ground_truth = item["ground_truth"]

        print(f"[{i+1}/{len(dataset)}] Running: {question}")

        try:
            answer, sources, contexts = pipeline.query(question)
            print(f"  ✓ Got answer ({len(contexts)} chunks retrieved)")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            continue

        results.append({
            "question":     question,
            "answer":       answer,
            "contexts":     contexts if isinstance(contexts, list) else [contexts],
            "ground_truth": ground_truth
        })

    return results
    
def build_ragas_dataset(results):
    return Dataset.from_dict({
        "user_input":          [r["question"]     for r in results],
        "response":            [r["answer"]       for r in results],
        "retrieved_contexts":  [r["contexts"]     for r in results],
        "reference":           [r["ground_truth"] for r in results]
    })

def save_results(scores):
    os.makedirs("eval/results", exist_ok=True)

    scores_dict = {}
    for metric in ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]:
        values = scores[metric]
        if isinstance(values, list):
            avg = sum(v for v in values if v is not None) / len([v for v in values if v is not None])
            scores_dict[metric] = round(avg, 4)
        else:
            scores_dict[metric] = round(values, 4)

    with open(RESULTS_PATH, "w") as f:
        json.dump(scores_dict, f, indent=2)

    print(f"\nResults saved to {RESULTS_PATH}")
    return scores_dict
    
def main():
    print("Loading test dataset")
    dataset = load_dataset()

    print("\nInitializing RAG pipeline")
    pipeline = RAGPipeline()

    print("\nRunning pipeline on test questions")
    results = run_pipeline_on_dataset(pipeline, dataset)

    print("\nBuilding RAGAS dataset")
    ragas_dataset = build_ragas_dataset(results)

    judge_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    judge_embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

    print("\nRunning evaluation")

    scores = evaluate(
        dataset=ragas_dataset,
        metrics=[
        Faithfulness(),
        AnswerRelevancy(),
        ContextPrecision(),
        ContextRecall()
        ],
        llm=judge_llm,
        embeddings=judge_embedding_model
    )

    scores_dict = save_results(scores)

    print("\n=== RAGAS Scores ===")
    for metric, score in scores_dict.items():
        print(f"{metric:<25} {score}")

if __name__ == "__main__":
    main()
