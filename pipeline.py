import os
import csv
from datetime import datetime
from rag.retriever import Retriever
from rag.generator import Generator

class Pipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()

    def run(self, query, top_k=3):
        top_matches = self.retriever.search(query, top_k=top_k)
        response = self.generator.generate_response(query, top_matches, top_k)
        self.log_interaction(query, top_matches, response)
        return response

    def log_interaction(self, query, top_matches, response, log_path="logs/conversations.csv"):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # Prepare a structured row for CSV
        timestamp = datetime.now().isoformat()
        match_details = [
            {"query": q, "response": a, "score": s}
            for q, a, s in top_matches
        ]

        # Flatten match details to string
        context_str = "\n\n".join([f"Q: {m['query']}\nA: {m['response']}\nScore: {m['score']}" for m in match_details])

        with open(log_path, mode="a", newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "user_query", "retrieved_context", "response"])
            if csvfile.tell() == 0:
                writer.writeheader()  # Write header only once
            writer.writerow({
                "timestamp": timestamp,
                "user_query": query,
                "retrieved_context": context_str,
                "response": response
            })

        print(f"📝 Logged interaction at {timestamp}")
