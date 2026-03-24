# Architecture Documentation

**Last Updated:** 2026-03-24

---

## Overview

Personal portfolio + AI Avatar assistant. Two main components:
1. **Static Website** — Jekyll on GitHub Pages
2. **AI Avatar Backend** — FastAPI on Google Cloud Run

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                     GitHub Pages                          │
│  Jekyll site: Cases, Industries, Domains, Roles pages    │
│  AI Avatar widget (widget.js + widget.css)                │
└──────────────────────┬───────────────────────────────────┘
                       │ REST /api/projects?industry=...
                       │ WebSocket /ws/chat
                       ▼
┌──────────────────────────────────────────────────────────┐
│              Google Cloud Run  (ai-avatar)                │
│                                                           │
│  FastAPI  ─  routers/                                     │
│    chat.py       /ws/chat  (WebSocket + RAG)              │
│    projects.py   /api/projects, /api/projects/{code}      │
│    contacts.py   /api/contacts, /api/contacts/{id}        │
│    health.py     /api/health, /                           │
│                                                           │
│  services/rag_service.py                                  │
│    vector search  →  knowledge_chunks (pgvector)          │
│    keyword fallback  →  in-memory KB docs                 │
│    Gemini 2.5 Flash  →  response generation               │
│                                                           │
│  app/db.py  →  psycopg_pool.ConnectionPool (min=1 max=5) │
└──────────────┬───────────────────────────────────────────┘
               │ psycopg3
               ▼
┌──────────────────────────────────────────────────────────┐
│              Neon PostgreSQL                              │
│  projects, project_industries, project_domains,           │
│  project_roles, contacts,                                 │
│  knowledge_chunks (pgvector, 587 chunks),                 │
│  chat_sessions, chat_messages                             │
└──────────────────────────────────────────────────────────┘
               ▲
               │ Gemini Embedding API (REST v1beta)
               │ scripts/generate_embeddings.py
               │ (runs in GitHub Actions on every deploy)
```

---

## Component Details

### 1. Static Website (Jekyll)

**Stack:** Jekyll 3.9, Minima theme, GitHub Pages

**Navigation pages:**
- `index.md` — Profile / M-Shape manifesto
- `business-challenges.md` — Problem-solution framing
- `services/index.md` — Launcher & Troubleshooter offering
- `cases.md` — Dynamic project portfolio with JS filtering
- `approach.md` — Entropy Reduction philosophy
- `articles.md` — Field Notes & System Design

**Dynamic experience pages** (thin Jekyll shell + JS fetch):
- `industries/*.md` — 8 industry pages (e.g. `retail`, `fintech`, `it-services`)
- `domains/*.md` — ~20 domain pages (e.g. `analytics`, `process-automation`)
- `roles/*.md` — 6 role pages (e.g. `enterprise-architect`, `solution-architect`)

Each page has `page_type` + `page_key` frontmatter. `assets/js/projects-dynamic.js` reads these and calls `/api/projects?industry=|domain=|role=<page_key>` to render projects dynamically.

**Key files:**
- `_config.yml` — Jekyll configuration
- `_layouts/` — custom layouts embedding AI widget
- `assets/main.scss` — CSS overrides (must be `.scss`, not `.css`)
- `assets/js/projects-dynamic.js` — shared dynamic rendering script

---

### 2. AI Avatar Backend

**Location:** `digital-avatar/backend/`

```
digital-avatar/backend/
├── app/
│   ├── main.py              # FastAPI app + lifespan (pool init)
│   ├── db.py                # ConnectionPool singleton
│   ├── deps.py              # RAGService singleton
│   ├── chat_log.py          # Chat session/message logging to Neon
│   ├── routers/
│   │   ├── chat.py          # /ws/chat WebSocket
│   │   ├── projects.py      # /api/projects, /api/projects/{code}
│   │   ├── contacts.py      # /api/contacts, /api/contacts/{id}
│   │   └── health.py        # /api/health, /
│   └── services/
│       └── rag_service.py   # RAG logic + Gemini integration
├── sql/
│   ├── chat_logs.sql        # DDL: chat_sessions, chat_messages
│   └── vector_search.sql    # DDL: knowledge_chunks + HNSW index
├── Dockerfile
├── requirements.txt
└── .env                     # local dev only, not in repo
```

**Environment variables (Cloud Run):**
| Variable | Required | Purpose |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Gemini AI + Embedding API |
| `NEON_DATABASE_URL` | Yes | PostgreSQL connection string |
| `TELEGRAM_BOT_TOKEN` | Yes | Session-end notifications |
| `TELEGRAM_CHAT_ID` | Yes | Target Telegram chat |
| `TELEGRAM_NOTIFY_ENABLED` | No | Set `false` to disable notifications |

---

### 3. RAG Service (`rag_service.py`)

**Priority order for context retrieval:**
1. **Vector search** (if `knowledge_chunks` is populated): embeds query via Gemini Embedding API, cosine similarity `ORDER BY embedding <=> %s::vector LIMIT 8`
2. **Keyword fallback**: word-boundary overlap scoring over in-memory KB docs

**Knowledge base loading (in-memory, keyword fallback):**
- Reads `.md`/`.txt` from `digital-avatar/backend/knowledge_base/` (auto-synced during deploy)
- Also loads root-level: `profile.md`, `business-challenges.md`, `index.md`

**System prompt sections (11 sections):**
1. Core Identity & Value Proposition
2. Professional Expertise
3. Professional Philosophy
4. Engagement Filters
5. Specialization Profile (M-Shape — only on request)
6. Qualifying Questions
7. Tone of Voice
8. **Project Codes — STRICTLY INTERNAL** (never expose codes like RTK-PROTEUS in responses)
9. Language Rules (English default; Russian if user writes in Russian)
10. Link Sharing Capability
11. Resume Generation Capability

---

### 4. Neon Database Schema

```sql
-- Projects and taxonomy
projects (id, code, title, industry, domain, role, employer, ...)
project_industries (project_id, slug)
project_domains    (project_id, slug)
project_roles      (project_id, slug)
contacts (id, ...)

-- Vector search
knowledge_chunks (
  id            SERIAL PRIMARY KEY,
  source        TEXT,          -- file path or 'db:projects'
  chunk_index   INT,
  content       TEXT,
  embedding     vector(768)    -- gemini-embedding-001
)
-- HNSW index: CREATE INDEX ON knowledge_chunks USING hnsw (embedding vector_cosine_ops)

-- Chat logging
chat_sessions  (id, started_at, ended_at, ip, ...)
chat_messages  (id, session_id, role, content, created_at)
```

**Source of truth:** Neon DB is always more current than `_projects/*.md` frontmatter. When in doubt, trust Neon.

---

### 5. Deployment

**Frontend (automatic):**
- Push to `main` → GitHub Actions builds Jekyll → GitHub Pages

**Backend (automatic via GitHub Actions `.github/workflows/deploy-backend.yml`):**
1. Checkout repo
2. Run `scripts/generate_kb.py` — sync knowledge base files into Docker context
3. Run `scripts/generate_embeddings.py` — embed KB chunks into Neon via Gemini API (`continue-on-error: true`)
4. Build Docker image (`linux/amd64`)
5. Push to Google Artifact Registry
6. Deploy to Cloud Run with env vars

**Environment variables injected into Cloud Run from GitHub Secrets:**
`GEMINI_API_KEY`, `NEON_DATABASE_URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

---

### 6. Data Flow

**User chat:**
```
User → widget.js (WebSocket) → /ws/chat
  → RAGService.generate_response(query, history)
    → vector search (Neon pgvector) OR keyword fallback
    → Gemini 2.5 Flash → response text
  → chat_log.py logs session/messages to Neon
  → on session end: Telegram notification sent
```

**Dynamic pages:**
```
Browser → /industries/retail (Jekyll page)
  → projects-dynamic.js reads page_type + page_key
  → fetch /api/projects?industry=retail
  → projects.py queries Neon junction tables by slug
  → renders project cards
```

**Embeddings update (on every deploy):**
```
scripts/generate_embeddings.py
  → load project texts from Neon (projects table)
  → load KB .md/.txt files
  → chunk each document
  → POST /v1beta/models/gemini-embedding-001:embedContent (one at a time)
  → upsert into knowledge_chunks (delete stale, insert new)
```

---

## Security

- API keys stored only in Cloud Run env vars / GitHub Secrets — never committed
- Project codes (RTK-PROTEUS etc.) never exposed in bot responses (enforced via system prompt §8)
- CORS: backend allows GitHub Pages domain + localhost
- WebSocket: public, no auth (rate limiting recommended)

---

## Quick Reference

```bash
# Local Jekyll
bundle exec jekyll serve

# Local backend
cd digital-avatar/backend
source .venv/bin/activate
uvicorn app.main:app --reload

# Manually regenerate embeddings
cd /path/to/repo
GEMINI_API_KEY=... NEON_DATABASE_URL=... python scripts/generate_embeddings.py

# Force GitHub Pages rebuild
git commit --allow-empty -m "Force rebuild" && git push
```
