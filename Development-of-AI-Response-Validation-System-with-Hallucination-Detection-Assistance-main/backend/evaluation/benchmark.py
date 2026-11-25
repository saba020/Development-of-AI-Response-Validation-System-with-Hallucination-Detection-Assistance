"""Benchmark runner for automated dataset evaluations."""
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from main import evaluate_ai_response
    from .metrics import calculate_evaluation_metrics
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from main import evaluate_ai_response
    from evaluation.metrics import calculate_evaluation_metrics


BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"


def load_dataset_samples(filename: str, sample_size: int = 10) -> List[Dict[str, Any]]:
    """Load sample records from a processed JSONL file."""
    file_path = PROCESSED_DATA_DIR / filename
    records = []

    if not file_path.exists():
        print(f"Dataset file not found: {file_path}")
        return records

    with open(file_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if idx >= sample_size:
                break
            line = line.strip()
            if line:
                records.append(json.loads(line))

    return records


def run_benchmark(
    dataset_name: str = "halueval_processed.jsonl",
    sample_size: int = 5
) -> Optional[Dict[str, Any]]:
    """Run benchmark evaluation on a subset of the dataset."""
    records = load_dataset_samples(dataset_name, sample_size=sample_size)
    if not records:
        print(f"No records found in {dataset_name}.")
        return None

    print(f"\n================ BENCHMARK RUN: {dataset_name} ================")
    print(f"Evaluating {len(records)} samples using multi-agent pipeline...\n")

    results = []
    start_time = time.perf_counter()

    for idx, record in enumerate(records, 1):
        question = record.get("question", "")
        ai_response = record.get("ai_response", record.get("reference_answer", ""))
        reference_answer = record.get("reference_answer", "")

        print(f"[{idx}/{len(records)}] Evaluating: {question[:60]}...")
        try:
            eval_result = evaluate_ai_response(
                question=question,
                ai_response=ai_response,
                reference_answer=reference_answer
            )
            results.append(eval_result)
        except Exception as e:
            print(f"  Error on item {idx}: {e}")

    total_time = time.perf_counter() - start_time
    metrics = calculate_evaluation_metrics(results)
    metrics["total_elapsed_seconds"] = round(total_time, 2)

    print("\n================ BENCHMARK REPORT ================")
    print(json.dumps(metrics, indent=2))
    print("==================================================\n")
    return metrics


if __name__ == "__main__":
    run_benchmark(sample_size=3)
