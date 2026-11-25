from pathlib import Path
from dotenv import dotenv_values
import os
from google import genai

BASE_DIR = Path(__file__).resolve().parent
config = dotenv_values(BASE_DIR / ".env")

api_key = config.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
model = config.get("GEMINI_MODEL") or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not api_key or api_key == "your_gemini_api_key_here":
    print("ERROR: GEMINI_API_KEY is not configured.")
    print("Please set your GEMINI_API_KEY in backend/.env or as an environment variable.")
    exit(1)

client = genai.Client(api_key=api_key)

print("Testing model:", model)

response = client.models.generate_content(
    model=model,
    contents="Explain photosynthesis in two sentences."
)

print("\nGemini response:")
print(response.text)
