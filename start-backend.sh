#!/bin/bash
# Start the FastAPI backend server

cd "$(dirname "$0")/backend"
source venv/bin/activate
uvicorn app.main:app --reload
