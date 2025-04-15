import gradio as gr
from pipeline import Pipeline

# Load the RAG pipeline once
rag_pipeline = Pipeline()

def generate_response(user_query):
    return rag_pipeline.run(user_query)

# Create a Gradio Interface
demo = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Ask your support question..."),
    outputs="text",
    title="Customer Support AI Assistant",
    description="Ask a support question and get an AI-generated response using RAG!"
)

if __name__ == "__main__":
    demo.launch()
