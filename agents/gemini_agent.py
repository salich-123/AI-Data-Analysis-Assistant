
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def ask_gemini(question):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key not found. Please configure your .env file."

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=question
        )

        return response.text

    except Exception as e:
        return f"Gemini API error: {e}"

