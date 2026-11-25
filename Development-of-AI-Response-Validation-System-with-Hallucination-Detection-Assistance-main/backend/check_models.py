from pathlib import Path
from dotenv import dotenv_values
import os
from google import genai

env_path = Path(__file__).resolve().parent / ".env"
config = dotenv_values(env_path)
api_key = config.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "your_gemini_api_key_here":
    print("ERROR: GEMINI_API_KEY is not configured.")
    print("Please set your GEMINI_API_KEY in backend/.env or as an environment variable.")
    exit(1)

client = genai.Client(api_key=api_key)

print("Available Gemini models:")
for model in client.models.list():
    if "generateContent" in (model.supported_actions or []):
        print(f" - {model.name}")
