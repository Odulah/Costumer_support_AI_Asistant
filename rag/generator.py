import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Generator:
    def __init__(self):
        # Load API key from environment
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_api_key:
            raise ValueError("❌ OPENROUTER_API_KEY not found in environment variables!")

        # Set OpenRouter endpoint and headers
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json"
        }

        # Set the model
        self.model = "mistralai/mistral-7b-instruct"

    def generate_response(self, query, top_matches, top_k=3):
        top_matches = top_matches[:top_k]
        context = "\n".join([f"Q: {q}\nA: {a}" for q, a, _ in top_matches])

        prompt = f"""You are a helpful customer support assistant. Use the context below to answer the question.

Context:
{context}

Question: {query}
Answer:"""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant for customer support."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        except requests.exceptions.HTTPError as http_err:
            return f"❌ OpenRouter API error: {http_err.response.status_code}\n{http_err.response.text}"
        except Exception as e:
            return f"⚠️ Unexpected error: {e}"
