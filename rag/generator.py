import requests
import os
from dotenv import load_dotenv

class Generator:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()

        # Get the key from environment
        hf_api_key = os.getenv("HF_API_KEY")
        if not hf_api_key:
            raise ValueError("❌ HF_API_KEY not found in environment variables!")

        # Use a lightweight, free model
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
        self.headers = {
            "Authorization": f"Bearer {hf_api_key}"
        }

    def generate_response(self, query, top_matches, top_k=3):
        top_matches = top_matches[:top_k]
        context = "\n".join([f"Q: {q}\nA: {a}" for q, a, _ in top_matches])

        prompt = f"""Answer the following question based on the provided context.

Context:
{context}

Question: {query}
Answer:"""

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            generated_text = response.json()[0].get("generated_text", "")
            return generated_text.split("Answer:")[-1].strip()
        except requests.exceptions.HTTPError as http_err:
            return f"❌ Hugging Face API error: {http_err.response.status_code}\n{http_err.response.text}"
        except Exception as e:
            return f"⚠️ Unexpected error: {e}"
