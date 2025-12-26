from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import os
from pathlib import Path
from dotenv import load_dotenv
from app.services.rag_service import RAGService

# Load environment variables
load_dotenv()

# Initialize Services
rag_service = RAGService()


app = FastAPI(title="Digital Avatar API")

# CORS middleware - Allow GitHub Pages and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vkgeorgia.github.io",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (Frontend)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Ensure the directory exists before mounting to avoid errors during startup if path is wrong
if not FRONTEND_DIR.exists():
    logger.error(f"Frontend directory not found at {FRONTEND_DIR}")
else:
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def root():
    return {"message": "Digital Avatar Backend is running"}

@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")
            
            # Use RAG service to generate response
            try:
                response_text = await rag_service.generate_response(data)
            except Exception as e:
                import traceback
                with open("debug_log_main.txt", "w") as f:
                    f.write(traceback.format_exc())
                logger.error(f"Error generating response: {e}")
                response_text = "Internal Error: Could not generate response."
            
            # Send text back to UI
            await websocket.send_text(response_text)
            
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error: {e}")
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
