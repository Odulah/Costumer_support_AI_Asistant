from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import Pipeline
from datetime import datetime, timezone
import json
import os

# Initialize FastAPI app
app = FastAPI()

# Initialize the Pipeline class
rag_pipeline = Pipeline()

# Define a Pydantic model for the input query
class Query(BaseModel):
    user_query: str

# Endpoint to generate a response
@app.post("/generate_response")
async def generate_response(query: Query):
    # Use the pipeline to generate a response
    response = rag_pipeline.run(query.user_query)

    # Log the interaction
    log_interaction(query.user_query, response)

    return {"response": response}

# Helper function to log interactions in a JSON file
def log_interaction(user_query, response, log_path="logs/interactions.json"):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    interaction = {
        "user_query": user_query,
        "response": response,
        "timestamp": str(datetime.now())
    }

    # Append the interaction to the JSON log file
    if os.path.exists(log_path):
        with open(log_path, "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append(interaction)

    with open(log_path, "w") as file:
        json.dump(data, file, indent=4)

    print(f"📝 Logged interaction: {user_query} -> {response}")
