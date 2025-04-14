# build_index.py
import pandas as pd
from rag.embedder import Embedder
from rag.vector_store import VectorStore  # adjust the import path if needed

# Step 1: Sample data (replace with your real data if needed)
data = {
    "input": [
        "How can I reset my password?",
        "What is your return policy?",
        "Where can I download the invoice?"
    ],
    "output": [
        "You can reset your password by clicking 'Forgot Password' on the login page.",
        "You can return items within 30 days of receipt.",
        "Invoices can be downloaded from the billing section of your account."
    ]
}

df = pd.DataFrame(data)

# Step 2: Build and save the index
embedder = Embedder()
vector_store = VectorStore(embedder)
vector_store.build_index(df)
vector_store.save_index(index_path="dataset/storage/faiss_index.index", mapping_path="dataset/storage/mapping.pkl")
