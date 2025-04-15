import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'rag')))

import os
import csv
from datetime import datetime
from rag.retriever import Retriever
from rag.generator import Generator

class Pipeline:
    def __init__(self):
        try:
            print("🔧 Initializing retriever and generator...")
            self.retriever = Retriever()
            self.generator = Generator()
            print("✅ Pipeline initialized successfully.")
        except Exception as e:
            print(f"❌ Error initializing Pipeline: {e}")
            raise

    def run(self, query, top_k=3):
        try:
            print(f"\n🔍 Running pipeline for query: '{query}'")
            print("🔎 Step 1: Retrieving relevant past queries...")
            top_matches = self.retriever.search(query, top_k=top_k)
            print(f"✅ Retrieved {len(top_matches)} top matches.")

            print("🧠 Step 2: Generating response using LLM...")
            response = self.generator.generate_response(query, top_matches, top_k)
            print("✅ Response generated.")

            print("📁 Step 3: Logging interaction...")
            self.log_interaction(query, top_matches, response)
            print("✅ Interaction logged.\n")

            return response
        except Exception as e:
            print(f"❌ Error during run(): {e}")
            return "Sorry, something went wrong while processing your query."

    def log_interaction(self, query, top_matches, response, log_path="logs/conversations.csv"):
        try:
            os.makedirs(os.path.dirname(log_path), exist_ok=True)

            timestamp = datetime.now().isoformat()
            match_details = [
                {"query": q, "response": a, "score": s}
                for q, a, s in top_matches
            ]
            context_str = "\n\n".join([
                f"Q: {m['query']}\nA: {m['response']}\nScore: {m['score']}"
                for m in match_details
            ])

            with open(log_path, mode="a", newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "user_query", "retrieved_context", "response"])
                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow({
                    "timestamp": timestamp,
                    "user_query": query,
                    "retrieved_context": context_str,
                    "response": response
                })

            print(f"📝 Interaction logged at {timestamp}")
        except Exception as e:
            print(f"⚠️ Failed to log interaction: {e}")
