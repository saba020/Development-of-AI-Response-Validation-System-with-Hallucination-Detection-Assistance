from pathlib import Path
from dotenv import dotenv_values
import os
from google import genai

env_path = Path(__file__).resolve().parent / ".env"
config = dotenv_values(env_path)

api_key = config.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
model = config.get("GEMINI_MODEL") or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

print("Environment file:", env_path)
print("API key loaded:", bool(api_key))
print("Model:", model)

if not api_key or api_key == "your_gemini_api_key_here":
    raise ValueError("GEMINI_API_KEY is not configured. Please set your key in backend/.env or as an environment variable.")
# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Send a test prompt
response = client.models.generate_content(
    model=model,
    contents="Explain hallucination detection in AI in two sentences."
)

print("\nGemini connection successful!")
print("AI Response:")
print(response.text)