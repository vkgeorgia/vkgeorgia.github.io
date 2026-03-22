"""Application-level singletons, initialized once at import time."""
from app.services.rag_service import RAGService

rag_service = RAGService()
