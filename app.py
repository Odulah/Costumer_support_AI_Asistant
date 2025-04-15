from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from contextlib import asynccontextmanager
import json
import os
from pipeline import Pipeline

rag_pipeline = None  # Global pipeline object

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_pipeline
    print("🚀 Starting up... Initializing RAG pipeline")
    try:
        rag_pipeline = Pipeline()
        print("✅ RAG pipeline initialized successfully")
    except Exception as e:
        print(f"❌ RAG pipeline failed to initialize: {e}")
        rag_pipeline = None

    yield  # Ready for requests

    print("🛑 Shutting down FastAPI app...")

app = FastAPI(lifespan=lifespan)

class Query(BaseModel):
    user_query: str

@app.get("/")
def root():
    return {"message": "FastAPI app is live!"}

@app.get("/health")
def health_check():
    status = "ready" if rag_pipeline else "not ready"
    return {"status": status}

@app.post("/generate_response")
async def generate_response(query: Query):
    if not rag_pipeline:
        return {"error": "RAG Pipeline not initialized."}

    try:
        response = rag_pipeline.run(query.user_query)
        log_interaction(query.user_query, response)
        return {"response": response}
    except Exception as e:
        print(f"❌ Error while processing query: {e}")
        return {"error": "Failed to process query. Please try again later."}

def log_interaction(user_query, response, log_path="logs/interactions.json"):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    interaction = {
        "user_query": user_query,
        "response": response,
        "timestamp": str(datetime.now())
    }

    data = []
    if os.path.exists(log_path):
        try:
            with open(log_path, "r") as file:
                data = json.load(file)
        except Exception as e:
            print(f"⚠️ Failed to read log: {e}")

    data.append(interaction)

    try:
        with open(log_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"📝 Logged interaction")
    except Exception as e:
        print(f"⚠️ Failed to write log: {e}")
