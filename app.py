from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import Pipeline

# Load the RAG pipeline once
rag_pipeline = Pipeline()

# Create FastAPI app instance
app = FastAPI()

# Define the input and output models
class QueryRequest(BaseModel):
    user_query: str

class QueryResponse(BaseModel):
    response: str

@app.post("/generate_response", response_model=QueryResponse)
def generate_response(query: QueryRequest):
    # Generate the response using the RAG pipeline
    result = rag_pipeline.run(query.user_query)
    return QueryResponse(response=result)
