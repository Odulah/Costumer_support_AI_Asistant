import gradio as gr
from rag.pipeline import Pipeline

rag_pipeline = Pipeline()

def chat_with_ai(user_input):
    return rag_pipeline.run(user_input)

gradio_ui = gr.ChatInterface(
    fn=chat_with_ai,
    title="AI Support Assistant",
    description="Ask questions about subscriptions, orders, and refunds."
)
