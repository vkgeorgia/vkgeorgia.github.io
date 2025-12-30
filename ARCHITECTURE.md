# Software Architecture Documentation

## Overview

This repository contains a personal portfolio website with an integrated AI Avatar assistant. The system consists of two main components:
1. **Static Website** - Jekyll-based site hosted on GitHub Pages
2. **AI Avatar Backend** - Python FastAPI service deployed on Google Cloud Run

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Pages                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Static Website (Jekyll + Minima Theme)                │ │
│  │  - HTML/CSS/JavaScript                                 │ │
│  │  - Portfolio content (About, Services, Downloads)      │ │
│  │  - AI Avatar Widget (widget.js + widget.css)           │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ WebSocket
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Google Cloud Run (Backend)                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  FastAPI Application                                   │ │
│  │  - WebSocket endpoint (/ws/chat)                       │ │
│  │  - RAG Service (Retrieval-Augmented Generation)        │ │
│  │  - Gemini 2.5 Flash API integration                    │ │
│  │  - Knowledge Base loader                               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ API Calls
                            ↓
                  ┌──────────────────┐
                  │  Google Gemini   │
                  │  AI API          │
                  └──────────────────┘
```

---

## Component Details

### 1. Static Website (Frontend)

**Technology Stack:**
- **Jekyll 3.9** - Static site generator
- **Minima Theme** - Minimalist Jekyll theme (GitHub Pages compatible)
- **GitHub Pages** - Free hosting for static sites
- **Markdown** - Content format

**Key Files:**
- `_config.yml` - Jekyll configuration
- `_layouts/` - Custom layouts (home.html, page.html) with AI widget
- `_includes/footer.html` - Custom footer with social links
- `index.html` - Home page
- `about.md`, `services.md`, `downloads.md` - Main content pages
- `digital-avatar/frontend/` - AI Avatar widget files

**Features:**
- Responsive design
- SEO optimized (meta tags, Open Graph, Schema.org)
- Clean navigation (Home, About, Services, Downloads)
- Professional footer with contact links
- AI Avatar chat widget

**Deployment:**
- Automatic deployment via GitHub Actions
- Branch: `test-minima` (testing) or `main` (production)
- URL: https://vkgeorgia.github.io/

---

### 2. AI Avatar Widget (Frontend Component)

**Location:** `digital-avatar/frontend/`

**Files:**
- `widget.js` - Chat widget logic and WebSocket communication
- `widget.css` - Widget styling

**Features:**
- Floating chat button (bottom-right corner)
- WebSocket connection to backend
- Real-time message exchange
- Responsive design
- Auto-reconnect on connection loss

**Integration:**
- Loaded in custom layouts (`_layouts/home.html`, `_layouts/page.html`)
- Appears on all pages
- No dependencies - vanilla JavaScript

---

### 3. AI Avatar Backend

**Technology Stack:**
- **Python 3.11+**
- **FastAPI** - Modern web framework
- **Google Gemini 2.5 Flash** - AI model
- **WebSocket** - Real-time communication
- **Docker** - Containerization
- **Google Cloud Run** - Serverless deployment

**Location:** `digital-avatar/backend/`

**Structure:**
```
digital-avatar/backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   └── services/
│       ├── rag_service.py   # RAG logic + Gemini integration
│       └── did_service.py   # (Optional) D-ID integration
├── Dockerfile               # Container configuration
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (not in repo)
```

**Key Components:**

#### 3.1 FastAPI Application (`main.py`)
- WebSocket endpoint: `/ws/chat`
- CORS middleware for GitHub Pages
- Static file serving (if needed)
- Health check endpoint: `/`

#### 3.2 RAG Service (`rag_service.py`)
**Responsibilities:**
- Load knowledge base from local files
- Generate AI responses using Gemini
- Implement fallback keyword search

**Knowledge Base Loading:**
- Reads `.md`, `.txt`, `.pdf`, `.docx` files
- Searches in multiple directories:
  - `digital-avatar/backend/knowledge_base/`
  - `knowledge-base/` (repo root)
- Excludes `sources/` directories

**AI Response Generation:**
- Uses Gemini 2.5 Flash model
- System prompt defines AI personality (Valerii Korobeinikov)
- Context: First 3 documents from knowledge base
- Language detection: Responds in user's language
- First-person responses ("I have experience...")

**Prompt Guidelines:**
- Professional, business-appropriate tone
- Short responses after providing calendar link
- Redirect unrelated questions
- Calendar link: `https://calendar.app.google/YwmXZytfSQ2qWX4Z7`

---

### 4. Knowledge Base

**Location:** `knowledge-base/`

**Structure:**
```
knowledge-base/
├── experience/
│   └── ai-ml-experience.md    # AI/ML projects and skills
├── 3. projects-eng/           # Project descriptions
│   ├── 41. EPAM - ADNO-TRMS.md
│   ├── 42. Transitrix - TRANS-AIPOC.md
│   └── ...
└── (other categories)
```

**Content:**
- Professional experience
- Project descriptions
- Skills and certifications
- Consulting services
- Contact information

**Format:**
- Markdown files with metadata
- Structured sections
- Links to external resources

---

## Data Flow

### User Interaction Flow

1. **User opens website** → GitHub Pages serves static HTML
2. **User clicks AI Avatar button** → Widget opens chat interface
3. **User sends message** → Widget establishes WebSocket connection
4. **Message sent to backend** → Cloud Run receives message
5. **RAG Service processes** → Loads knowledge base, queries Gemini
6. **AI generates response** → Gemini returns answer
7. **Response sent to user** → WebSocket sends message back
8. **User sees response** → Widget displays AI message

### Knowledge Base Update Flow

1. **Update markdown files** in `knowledge-base/`
2. **Commit and push** to GitHub
3. **Backend deployment** (manual or automated)
   - Sync knowledge base to backend
   - Build Docker image
   - Deploy to Cloud Run
4. **AI uses updated content** in responses

---

## Deployment

### Frontend (GitHub Pages)

**Automatic Deployment:**
- Push to `test-minima` or `main` branch
- GitHub Actions builds Jekyll site
- Deploys to https://vkgeorgia.github.io/

**Configuration:**
- Repository Settings → Pages
- Source: Deploy from branch
- Branch: `test-minima` (or `main`)
- Folder: `/ (root)`

### Backend (Google Cloud Run)

**Manual Deployment:**
```bash
# 1. Sync knowledge base
cd digital-avatar/backend
rm -rf knowledge_base
mkdir knowledge_base
cp -r ../../knowledge-base/* knowledge_base/

# 2. Build Docker image
docker build -t gcr.io/PROJECT_ID/ai-avatar:latest .

# 3. Push to Google Container Registry
docker push gcr.io/PROJECT_ID/ai-avatar:latest

# 4. Deploy to Cloud Run
gcloud run deploy ai-avatar \
  --image gcr.io/PROJECT_ID/ai-avatar:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your-api-key
```

**Environment Variables:**
- `GEMINI_API_KEY` - Google Gemini API key (required)
- `KNOWLEDGE_BASE_DIR` - Custom knowledge base path (optional)

---

## Configuration Files

### `_config.yml` (Jekyll)
```yaml
title: "Valerii Korobeinikov"
description: "Enterprise Architect and IT Consultant"
theme: minima
author: Valerii Korobeinikov
email: vkgeorgia@icloud.com

# Navigation
header_pages:
  - about.md
  - services.md
  - downloads.md

# Exclude from processing
exclude:
  - digital-avatar/backend
  - knowledge-base/*/sources/
  - projects/
  - industries/
  - roles/
```

### `Dockerfile` (Backend)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
COPY knowledge_base/ ./knowledge_base/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Security Considerations

1. **API Keys:**
   - Gemini API key stored in Cloud Run environment variables
   - Never committed to repository
   - Rotated periodically

2. **CORS:**
   - Backend allows only GitHub Pages domain
   - Localhost allowed for development

3. **WebSocket:**
   - No authentication (public chat)
   - Rate limiting recommended for production

4. **Knowledge Base:**
   - Public information only
   - No sensitive data in markdown files

---

## Monitoring & Logging

### Frontend
- GitHub Pages deployment logs
- Browser console for widget errors

### Backend
- Cloud Run logs (stdout/stderr)
- Python logging module
- Error tracking in `rag_service.py`

**Log Levels:**
- `INFO` - Normal operations
- `WARNING` - Missing files, API issues
- `ERROR` - Exceptions, failures

---

## Development Workflow

### Local Development

**Frontend:**
```bash
# Install Jekyll
gem install jekyll bundler

# Install dependencies
bundle install

# Run local server
bundle exec jekyll serve

# Open http://localhost:4000
```

**Backend:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your-key

# Run server
uvicorn app.main:app --reload

# Test WebSocket at ws://localhost:8000/ws/chat
```

### Testing

**Frontend:**
- Manual testing in browser
- Check responsive design
- Verify AI widget functionality

**Backend:**
- Test WebSocket connection
- Verify knowledge base loading
- Test AI responses
- Check error handling

---

## Future Improvements

1. **Backend:**
   - Add authentication for admin features
   - Implement rate limiting
   - Add conversation history
   - Improve knowledge base search (vector embeddings)
   - Add analytics/metrics

2. **Frontend:**
   - Add conversation history UI
   - Implement typing indicators
   - Add file upload for questions
   - Improve mobile experience

3. **Infrastructure:**
   - Automate backend deployment (CI/CD)
   - Add monitoring/alerting
   - Implement caching
   - Add load balancing

4. **AI:**
   - Fine-tune responses
   - Add multi-turn conversations
   - Implement context retention
   - Add voice interface

---

## Troubleshooting

### Common Issues

**1. AI Widget not appearing:**
- Check browser console for errors
- Verify `widget.js` and `widget.css` are loaded
- Check layout files include widget scripts

**2. WebSocket connection fails:**
- Verify backend is running
- Check CORS configuration
- Ensure correct backend URL in `widget.js`

**3. AI responses are generic:**
- Verify knowledge base is loaded
- Check backend logs for errors
- Ensure Gemini API key is valid

**4. Jekyll build fails:**
- Check `_config.yml` syntax
- Verify all files are valid Markdown
- Check for missing dependencies

---

## Contact & Support

**Repository:** https://github.com/vkgeorgia/vkgeorgia.github.io
**Website:** https://vkgeorgia.github.io
**Email:** vkgeorgia@icloud.com
**LinkedIn:** https://www.linkedin.com/in/valeriikorobeinikov/

---

## License

This project is private and proprietary. All rights reserved.

---

**Last Updated:** 2025-12-30
**Version:** 1.0 (Minima Theme)
