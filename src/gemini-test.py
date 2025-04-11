from google import genai

import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.environ.get("GEMINI_AI_API")

client = genai.Client(api_key=gemini_api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Hello! How are you? Can you explain how AI works in a few words"
)
print(response.text)
