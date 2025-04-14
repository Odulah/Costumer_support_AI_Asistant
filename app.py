from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from gradio_interface import gradio_ui

# FastAPI app instance
app = FastAPI()

# Enable CORS (optional, helpful if deploying)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Assistant API is live 🎉"}

# Mount the Gradio interface
@app.on_event("startup")
async def startup_event():
    gradio_ui.launch(server_name="0.0.0.0", server_port=7860, share=False, inline=False, inbrowser=False, show_api=False, prevent_thread_lock=True)
