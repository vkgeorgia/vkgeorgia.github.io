# Digital Avatar

AI-powered digital avatar for consulting services - an intelligent chatbot that represents Valerii Korobeinikov in conversations with recruiters and potential clients.

## Overview

The Digital Avatar is an AI system that uses information about professional experience, projects, and skills to conduct professional dialogues. It automates initial communication, presents expertise effectively, filters requests, and scales presence across multiple conversations.

## Project Structure

```
digital-avatar/
├── backend/          # FastAPI backend with WebSocket support
│   ├── app/         # Main application code
│   │   ├── main.py
│   │   └── services/
│   │       ├── rag_service.py    # RAG service for knowledge base
│   │       └── did_service.py    # DID service
│   ├── static/      # Static files
│   ├── requirements.txt
│   ├── Dockerfile
│   └── deploy.ps1   # Deployment script for Google Cloud Run
├── frontend/        # Web interface
│   ├── widget.js    # Chat widget for embedding
│   ├── widget.css   # Widget styles
│   ├── demo.html    # Demo page
│   ├── script.js
│   └── style.css
├── docs/            # Documentation
│   ├── spec.md      # Project specification
│   ├── plan.md      # Development plan
│   └── DEPLOY.md    # Deployment instructions
├── .env             # Environment variables (not in git)
└── google_credentials.json  # Google API credentials (not in git)
```

## Technology Stack

- **LLM**: Google Gemini (`gemini-2.5-flash`)
- **RAG**: Custom Python implementation with Google Drive knowledge base
- **Backend**: Python FastAPI with WebSocket
- **Frontend**: HTML/CSS/JavaScript (pure text chat)
- **Hosting**: GitHub Pages (frontend), Google Cloud Run (backend)

## Knowledge Base

The avatar uses the knowledge base from the valerii-site project:
- Project documentation from `/projects`
- Domain expertise from `/domains`
- Industry experience from `/industries`
- Role descriptions from `/roles`
- Source materials from `/sources`

## Setup

1. **Environment Variables**:
   - Copy `.env` and configure your API keys
   - Set `GEMINI_API_KEY` for Google Gemini access

2. **Google Credentials**:
   - Place `google_credentials.json` in this directory
   - Configure Google Drive API access

3. **Install Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run Backend**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

## Integration

The chat widget is integrated into the main site at `index.html`. To use it on other pages:

```html
<link rel="stylesheet" href="/digital-avatar/frontend/widget.css">
<script src="/digital-avatar/frontend/widget.js"></script>
```

## Documentation

- [Specification](docs/spec.md) - Detailed project specification
- [Development Plan](docs/plan.md) - Implementation roadmap
- [Deployment Guide](docs/DEPLOY.md) - Deployment instructions

## Features

- ✅ Real-time text chat via WebSocket
- ✅ RAG-based responses using knowledge base
- ✅ Google Drive integration for knowledge storage
- ✅ Embeddable chat widget
- 🚧 Google Calendar integration for meeting scheduling
- 🚧 Conversation history storage
- 🚧 Analytics and logging

## License

Private project - all rights reserved.
