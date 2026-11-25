"""Evaluation metrics calculator for AI Response Validation System."""
from typing import List, Dict, Any


def calculate_evaluation_metrics(evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate aggregate performance and quality metrics across a set of evaluations.

    Args:
        evaluations: List of evaluation dicts, each containing 'evaluation' and 'final_verdict'.

    Returns:
        Dictionary of aggregate quality statistics.
    """
    if not evaluations:
        return {
            "total_evaluations": 0,
            "average_overall_score": 0.0,
            "pass_rate": 0.0,
            "hallucination_rate": 0.0,
            "average_relevance": 0.0,
            "average_accuracy": 0.0,
            "average_completeness": 0.0,
            "verdict_distribution": {}
        }

    total = len(evaluations)
    overall_scores = []
    relevance_scores = []
    accuracy_scores = []
    completeness_scores = []
    hallucination_scores = []
    verdicts = {}
    pass_count = 0
    hallucinated_count = 0

    for item in evaluations:
        final_verdict = item.get("final_verdict", {})
        eval_details = item.get("evaluation", {})

        score = final_verdict.get("overall_score")
        if score is not None:
            overall_scores.append(score)

        verdict = final_verdict.get("final_verdict", "UNKNOWN")
        verdicts[verdict] = verdicts.get(verdict, 0) + 1
        if verdict in ("EXCELLENT", "GOOD", "Pass"):
            pass_count += 1

        # Agent dimension scores
        relevance = eval_details.get("relevance", {}).get("relevance_score")
        if relevance is not None:
            relevance_scores.append(relevance)

        accuracy = eval_details.get("accuracy", {}).get("accuracy_score")
        if accuracy is not None:
            accuracy_scores.append(accuracy)

        completeness = eval_details.get("completeness", {}).get("completeness_score")
        if completeness is not None:
            completeness_scores.append(completeness)

        hallucination = eval_details.get("hallucination", {}).get("hallucination_score")
        if hallucination is not None:
            hallucination_scores.append(hallucination)
            if hallucination >= 40:
                hallucinated_count += 1

    return {
        "total_evaluations": total,
        "average_overall_score": round(sum(overall_scores) / len(overall_scores), 2) if overall_scores else 0.0,
        "pass_rate": round((pass_count / total) * 100, 2),
        "hallucination_rate": round((hallucinated_count / total) * 100, 2),
        "average_relevance": round(sum(relevance_scores) / len(relevance_scores), 2) if relevance_scores else 0.0,
        "average_accuracy": round(sum(accuracy_scores) / len(accuracy_scores), 2) if accuracy_scores else 0.0,
        "average_completeness": round(sum(completeness_scores) / len(completeness_scores), 2) if completeness_scores else 0.0,
        "average_hallucination_risk": round(sum(hallucination_scores) / len(hallucination_scores), 2) if hallucination_scores else 0.0,
        "verdict_distribution": verdicts
    }
