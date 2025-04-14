#!/bin/bash

# Start FastAPI + Gradio combo
uvicorn app:app --host 0.0.0.0 --port 8000
