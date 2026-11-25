import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from rag.vector_store import get_vector_store
from utils.gemini_retry import generate_content_with_retry

# Load environment configuration
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

def get_client_and_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured. Please set your GEMINI_API_KEY in backend/.env")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return genai.Client(api_key=api_key), model


def retrieve_evidence(question, top_k=5):
    """Retrieve supporting documents from FAISS."""
    try:
        vector_store = get_vector_store()
        results = vector_store.search(
            query=question,
            top_k=top_k
        )
        evidence = []
        for result in results:
            document = result["document"]
            evidence.append({
                "source": document.get("source", "Unknown"),
                "similarity": round(result["score"], 4),
                "text": document["text"]
            })
        return evidence
    except Exception as e:
        print(f"Notice: FAISS retrieval unavailable ({e}). Evaluating against available context.")
        return []


def detect_hallucinations(
    question: str,
    ai_response: str,
    evidence=None
):
    """
    Detect fabricated, unsupported, or contradicted
    claims in an AI-generated response.
    """

    if evidence is None:
        evidence = retrieve_evidence(question)

    evidence_text = json.dumps(
        evidence,
        indent=2,
        ensure_ascii=False
    )

    prompt = f"""
You are an expert AI Hallucination Detection Agent.

Your responsibility is to identify fabricated,
unsupported, and evidence-contradicted claims.

USER QUESTION:
{question}

AI-GENERATED RESPONSE:
{ai_response}

RETRIEVED EVIDENCE:
{evidence_text if evidence else "No evidence retrieved."}

EVALUATION INSTRUCTIONS:

1. Break the AI response into individual factual claims.
2. Compare each claim against the retrieved evidence.
3. Identify claims directly contradicted by evidence.
4. Identify claims that are not supported by evidence.
5. Do not automatically classify every unsupported
   claim as a proven hallucination.
6. Distinguish contradicted claims from claims that
   simply lack sufficient evidence.
7. Treat retrieved documents as evidence, not as
   unquestionable truth.
8. Do not invent facts or supporting sources.
9. If evidence is insufficient, use the verdict
   INSUFFICIENT_EVIDENCE.
10. Give a hallucination risk score from 0 to 100
    only when there is sufficient evidence.

VERDICT DEFINITIONS:

NO_HALLUCINATION:
No hallucinated claims identified in the available evidence.

POSSIBLE_HALLUCINATION:
One or more claims lack sufficient supporting evidence.

HALLUCINATION:
One or more claims are contradicted by reliable evidence.

INSUFFICIENT_EVIDENCE:
There is not enough relevant evidence to evaluate the claims.

Return ONLY valid JSON in this format:

{{
    "hallucination_score": 0,
    "verdict": "NO_HALLUCINATION",
    "explanation": "Brief explanation",
    "hallucinated_claims": [],
    "unsupported_claims": [],
    "contradicted_claims": [],
    "evidence_used": []
}}

The hallucination score represents estimated risk:
0 means no hallucination identified;
100 means severe evidence-based contradiction.
"""

    client, model = get_client_and_model()

    response = generate_content_with_retry(
        client=client,
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        },
        max_attempts=3
    )

    try:
        result = json.loads(response.text)
    except (json.JSONDecodeError, TypeError):
        raise ValueError("Gemini returned invalid JSON.")

    return result


if __name__ == "__main__":

    question = "What is the capital of France?"

    ai_response = (
        "Paris is the capital of France. "
        "Paris is also the capital of Germany."
    )

    result = detect_hallucinations(
        question=question,
        ai_response=ai_response
    )

    print("\n===== HALLUCINATION DETECTION RESULT =====")
    print(json.dumps(result, indent=4))
