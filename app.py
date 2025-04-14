from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import Pipeline  # Make sure this is the correct import for your pipeline

app = FastAPI()

# Define request model for the user query
class QueryRequest(BaseModel):
    user_query: str  # The structure of the input query

# Initialize the RAG pipeline (ensure this is properly configured in your pipeline)
rag_pipeline = Pipeline()

@app.post("/generate_response")
async def generate_response(query: QueryRequest):
    """
    Accepts a user query and returns the AI-generated response.
    The AI model processes the query using the RAG pipeline.
    """
    try:
        # Process the user query through the pipeline
        response = rag_pipeline.run(query.user_query)
        return {"response": response}  # Return the AI response
    except Exception as e:
        # Handle any errors during the response generation process
        return {"error": str(e)}

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
