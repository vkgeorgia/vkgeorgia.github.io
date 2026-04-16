# vkgeorgia.github.io — AI Agent Instructions

## What this repo is

Jekyll static site (GitHub Pages) — personal portfolio and AI avatar for Valerii Korobeinikov.

**This repo = frontend only.** No backend code here.

---

## Architecture

```
vkgeorgia.github.io (this repo, public)
├── Jekyll static site (portfolio pages)
└── digital-avatar/frontend/
    ├── widget.js   ← chat widget, connects via WebSocket to backend
    └── widget.css

Backend (separate private repo: vkgeorgia/Jeeves)
└── chatbot/        ← FastAPI, deployed to Cloud Run
    └── connects to: chatbot-db (Neon PostgreSQL, separate project)
```

**Backend Cloud Run URL:** configured in `_config.yml` → `backend_url`

---

## Security architecture (updated 2026-04-17)

### Two separate databases
- **chatbot-db** (Neon, cloud) — only tables needed by the chatbot: chat sessions,
  contacts (lead capture), projects (read), owner profile (read), generated resumes,
  proposals, knowledge chunks
- **jeeves-db** (local PostgreSQL on server video) — full CRM, budget, strategy,
  agents data. Never accessible from the public internet.

### Secrets
- All backend secrets (`CHATBOT_DATABASE_URL`, `GEMINI_API_KEY`, etc.) stored in
  **GCP Secret Manager**, not in env files
- Deploy via `chatbot/deploy.sh` uses `--set-secrets` (not `--set-env-vars`)
- This repo's CI secrets (GitHub Secrets) contain only what's needed for deployment

### What NOT to put in this repo
- Any database connection strings
- API keys or tokens
- `.env` files (excluded via `.gitignore`)
- `.claude/` directory (excluded via `.gitignore` and global gitignore)

---

## Key files

| File | Purpose |
|------|---------|
| `_config.yml` | Jekyll config; `backend_url` → Cloud Run chatbot URL |
| `digital-avatar/frontend/widget.js` | Chat widget (Jekyll template, reads `backend_url`) |
| `digital-avatar/frontend/widget.css` | Widget styles |
| `.gitignore` | Excludes `.env`, `.claude/`, credentials |

---

## Backend repo context

Private repo: `vkgeorgia/Jeeves`

- `chatbot/` — the Cloud Run service this site connects to
- `chatbot/sql/chatbot_db_schema.sql` — schema for chatbot-db (Neon)
- `chatbot/deploy.sh` — deployment script (uses GCP Secret Manager)
- Jeeves bot runs locally on server video (192.168.50.31), uses local PostgreSQL

---

## Deploy

Site: automatic via GitHub Pages on push to `main`.

Chatbot backend: from Jeeves repo — `cd chatbot && ./deploy.sh`
