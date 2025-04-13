from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import Pipeline

app = FastAPI()

# Define request model for the user query
class QueryRequest(BaseModel):
    user_query: str

# Initialize the RAG pipeline
rag_pipeline = Pipeline()

@app.post("/generate_response")
async def generate_response(query: QueryRequest):
    """
    Accepts a user query and returns the AI-generated response.
    """
    response = rag_pipeline.run(query.user_query)
    return {"response": response}

@app.get("/")
async def root():
    """
    Simple root route for testing the API.
    """
    return {"message": "Welcome to the AI assistant!"}

@app.get("/favicon.ico")
async def favicon():
    """
    Route to handle favicon.ico requests (optional).
    """
    return {"message": "No favicon available"}
