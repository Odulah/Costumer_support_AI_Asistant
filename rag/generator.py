import requests
import os
from dotenv import load_dotenv

class Generator:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()

        # Get the key from environment
        hf_api_key = os.getenv("HF_API_KEY")

        self.api_url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
        self.headers = {
            "Authorization": f"Bearer {hf_api_key}"
        }

    def generate_response(self, query, top_matches, top_k=3):
        top_matches = top_matches[:top_k]
        context = "\n".join([f"Q: {q}\nA: {a}" for q, a, _ in top_matches])

        prompt = f"""You are a helpful customer support assistant. Use the past conversations to answer the query accurately.

Context:
{context}

User Query: {query}
Answer:"""

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            try:
                return response.json()[0]['generated_text'].split("Answer:")[-1].strip()
            except Exception:
                return "⚠️ Failed to parse model response."
        else:
            return f"❌ Hugging Face API error: {response.status_code}\n{response.text}"
