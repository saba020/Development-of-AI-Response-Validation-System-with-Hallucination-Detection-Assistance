
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import traceback

from main import evaluate_ai_response


app = FastAPI(
    title="AI Response Quality Evaluator API",
    description="Multi-agent AI response evaluation system",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "https://development-of-ai-response-validati-mu.vercel.app"
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class EvaluationRequest(BaseModel):
    question: str = Field(min_length=1)
    ai_response: str = Field(min_length=1)
    reference_answer: Optional[str] = ""


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "AI Response Quality Evaluator API is running!",
        "status": "active"
    }


# Health endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Response Quality Evaluator"
    }


# Favicon endpoint (suppresses browser 404 log noise)
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


# Evaluation endpoint
@app.post("/evaluate")
def evaluate(request: EvaluationRequest):

    try:
        print("\n========== NEW EVALUATION REQUEST ==========")

        print("Question:", request.question)
        print("Starting five-agent evaluation pipeline...")

        result = evaluate_ai_response(
            question=request.question,
            ai_response=request.ai_response,
            reference_answer=request.reference_answer or ""
        )

        print("Evaluation completed successfully!")
        print("============================================\n")

        return result

    except Exception as error:

        print("\n========== BACKEND ERROR ==========")
        traceback.print_exc()
        print("===================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"\n=======================================================")
    print(f"  AI Response Quality Evaluator API")
    print(f"  Running locally on http://{host}:{port}")
    print(f"  Documentation: http://{host}:{port}/docs")
    print(f"=======================================================\n")
    uvicorn.run("api:app", host=host, port=port, reload=True)

