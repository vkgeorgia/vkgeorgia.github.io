# Technical Specification: Resume Generation Service

**Version:** 1.1
**Date:** 2026-03-23
**For:** Claude Code (website backend implementation)
**Database:** Neon PostgreSQL (идентификатор проекта — только в консоли Neon, не в репозитории)
**Backend stack:** Python 3.11 + FastAPI + uvicorn, deployed on Google Cloud Run (`ai-avatar`, `us-central1`; номер GCP-проекта — в консоли Google Cloud, не хардкодить в доке)

> **Status:** Archived in this repository.
> Active backend implementation ownership moved to:
> **https://github.com/vkgeorgia/Jeeves**

---

## Overview

Add a resume generation API endpoint to the existing website backend. The endpoint receives a job vacancy description, queries the Neon database for relevant projects and rules, calls the Claude API to generate a tailored resume, saves the result, and returns it.

The service must be **reusable** — called by both the website chatbot and other clients (Cowork agent, future automations).

---

## Endpoint Specification

### `POST /api/resume/generate`

**Auth:** Internal API key via `x-api-key` header (same pattern as other protected endpoints, or add `RESUME_API_KEY` env variable).

#### Request Body

```json
{
  "vacancy_text": "string, required — full text of the job description",
  "vacancy_url": "string, optional — source URL (LinkedIn etc.)",
  "role_hint": "string, optional — e.g. 'enterprise-architect', 'business-analyst'",
  "industry_hint": "string, optional — e.g. 'finance', 'retail', 'manufacturing'",
  "chat_session_id": "uuid, optional — link to active chat session",
  "contact_id": "integer, optional — link to known contact/lead",
  "notes": "string, optional — any context for this generation"
}
```

#### Response — 200 OK

```json
{
  "id": "uuid",
  "slug": "string — e.g. 'ea-finance-2026-03-23'",
  "title": "string — e.g. 'Enterprise Architect – Coca-Cola Hellenic'",
  "content_md": "string — full resume in markdown",
  "created_at": "ISO timestamp"
}
```

#### Response — 400 Bad Request

```json
{ "error": "vacancy_text is required" }
```

#### Response — 500 Internal Server Error

```json
{ "error": "Generation failed", "detail": "..." }
```

---

### `GET /api/resume/:slug`

Returns a previously generated resume by slug.

#### Response — 200 OK

```json
{
  "id": "uuid",
  "slug": "string",
  "title": "string",
  "content_md": "string",
  "target_role": "string",
  "target_company": "string",
  "status": "string",
  "created_at": "ISO timestamp"
}
```

#### Response — 404

```json
{ "error": "Resume not found" }
```

---

### `PATCH /api/resume/:slug/status`

Update the status of a resume (e.g. mark as sent).

#### Request Body

```json
{
  "status": "sent | viewed | draft | ready",
  "sent_to": "string, optional",
  "sent_at": "ISO timestamp, optional"
}
```

---

## Generation Algorithm

The endpoint must execute the following steps **in order**:

### Step 1 — Analyze Vacancy

Extract from `vacancy_text`:
- `target_role` — infer role slug: `enterprise-architect`, `business-analyst`, `project-manager`, `consultant`, `product-manager`
- `target_company` — company name if mentioned
- `target_industry` — primary industry: `finance`, `retail`, `manufacturing`, `telecom`, `oil-gas`, `aviation`, `healthcare`, `consulting`
- `target_domains` — array of functional domain keywords found in the text (e.g. `["ERP", "Supply Chain", "Finance", "TOGAF"]`)
- `slug` — generate as `{role}-{company-slug}-{YYYY-MM-DD}`, e.g. `ea-cch-2026-03-23`
- `title` — generate as `{Role Title} – {Company}`, e.g. `Enterprise Architect – Coca-Cola Hellenic`

### Step 2 — Load Rules from DB

```sql
SELECT category, rule, applies_to
FROM resume_rules
WHERE applies_to = 'all'
   OR applies_to LIKE '%' || $target_role || '%'
   OR applies_to LIKE '%' || $target_industry || '%'
ORDER BY category, id;
```

### Step 3 — Score and Select Projects

```sql
SELECT
  id, code, title, employer, client, industry, domain, role,
  year_start, year_end, key_result, executive_md,
  -- Scoring (inline for simplicity, can be refactored):
  (
    CASE WHEN role ILIKE '%' || $role_keyword || '%' THEN 3 ELSE 0 END +
    CASE WHEN industry ILIKE '%' || $industry_keyword || '%' THEN 2 ELSE 0 END +
    CASE WHEN industry ILIKE ANY($adjacent_industries) THEN 1 ELSE 0 END +
    -- domain keywords: +2 for first match, +1 for each additional
    (SELECT COUNT(*) * 2 FROM unnest($domain_keywords::text[]) kw
     WHERE domain ILIKE '%' || kw || '%' LIMIT 1) +
    (SELECT GREATEST(COUNT(*) - 1, 0) FROM unnest($domain_keywords::text[]) kw
     WHERE domain ILIKE '%' || kw || '%')
  ) AS score
FROM projects
WHERE year_end >= (EXTRACT(YEAR FROM NOW()) - 10)  -- last 10 years
   OR (
     -- include older projects only if direct domain match
     domain ILIKE ANY($domain_like_patterns)
   )
ORDER BY score DESC, year_end DESC NULLS LAST
LIMIT 12;  -- fetch top 12, LLM will pick best 6-8
```

### Step 4 — Load Owner Profile

```sql
SELECT email, linkedin_url, website_url, location, bio
FROM owner_profile
WHERE id = 1;
```

### Step 5 — Load Role Summary (if available)

```sql
SELECT title, description_md
FROM roles
WHERE slug = $target_role;
```

### Step 6 — Call Claude API

Compose and send a prompt to the Claude API. Use model `claude-opus-4-6` or `claude-sonnet-4-6`.

#### System Prompt

```
You are a professional resume writer generating tailored resumes for Valerii Korobeinikov.
You must follow ALL rules provided. You must use ONLY the project data provided — do not invent or assume any experience.
Output clean markdown only — no explanations, no comments, no preamble.
```

#### User Prompt Structure

```
## RULES
{all rules from Step 2, formatted as numbered list}

## VACANCY
{vacancy_text}

## EXTRACTED VACANCY ANALYSIS
Role: {target_role}
Industry: {target_industry}
Key domains: {target_domains joined by ", "}
Company: {target_company}

## OWNER PROFILE
Email: {email}
LinkedIn: {linkedin_url}
Location: {location}

Bio summary:
{first 500 chars of bio}

## ROLE SUMMARY (for Summary section framing)
{description_md from roles table, or empty if not found}

## AVAILABLE PROJECTS (scored by relevance, pick best 6-8)
{for each project in scored list:}
---
Code: {code}
Title: {title}
Client: {client} | Employer: {employer}
Industry: {industry} | Domain: {domain}
Role: {role} | Period: {year_start}–{year_end}
Key result: {key_result}
Executive description:
{executive_md}

## TASK
Generate a complete, tailored resume in markdown format for the vacancy above.
Apply all rules. Select 6-8 most relevant projects.
Return ONLY the markdown — no commentary before or after.
```

### Step 7 — Save to Database

```sql
INSERT INTO generated_resumes (
  slug, title, target_role, target_company, target_industry,
  vacancy_text, vacancy_url, content_md,
  status, source, chat_session_id, contact_id, notes
) VALUES (
  $slug, $title, $target_role, $target_company, $target_industry,
  $vacancy_text, $vacancy_url, $content_md,
  'ready', 'bot', $chat_session_id, $contact_id, $notes
)
ON CONFLICT (slug) DO UPDATE
  SET content_md = EXCLUDED.content_md,
      status = 'ready'
RETURNING id, slug, title, content_md, created_at;
```

### Step 8 — Return Response

Return the result from Step 7.

---

## Database Tables Used (all exist, no migrations needed)

| Table | Usage |
|---|---|
| `resume_rules` | Generation rules (38 rows across 14 categories) |
| `projects` | Source project data (43 projects, with `executive_md`) |
| `owner_profile` | Contact info and bio (1 row) |
| `roles` | Role summaries (2 rows: enterprise-architect, business-analyst) |
| `generated_resumes` | Output storage — insert here after generation |
| `contacts` | Optional FK for linking resume to a lead |
| `chat_sessions` | Optional soft reference — no FK constraint (table may not exist in current schema) |

### `generated_resumes` table schema

```sql
CREATE TABLE generated_resumes (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  slug            text UNIQUE NOT NULL,
  title           text NOT NULL,
  target_role     text,
  target_company  text,
  target_industry text,
  vacancy_text    text,
  vacancy_url     text,
  content_md      text NOT NULL,
  preset_slug     text,
  status          text NOT NULL DEFAULT 'draft',  -- draft | ready | sent | viewed
  source          text NOT NULL DEFAULT 'manual', -- manual | bot
  contact_id      integer REFERENCES contacts(id) ON DELETE SET NULL,
  chat_session_id uuid,  -- soft reference; no FK constraint (chat_sessions table may not exist yet)
  sent_at         timestamptz,
  sent_to         text,
  notes           text,
  created_at      timestamptz DEFAULT now(),
  updated_at      timestamptz DEFAULT now()
);
```

---

## Environment Variables Required

```env
# Already exists in Cloud Run (no change needed):
GEMINI_API_KEY=...             # Already set — used by existing /ws/chat (fallback LLM)
NEON_DATABASE_URL=postgresql://...neon...  # Already set — Neon connection string

# New — add to Cloud Run environment + .env:
ANTHROPIC_API_KEY=sk-ant-...   # New — PRIMARY LLM for resume generation (Claude API)
RESUME_API_KEY=...             # New — secret header for protecting /api/resume/* endpoints
```

> **Note:** The existing backend uses `NEON_DATABASE_URL` (not `DATABASE_URL`). Use this variable name throughout.

### LLM Selection Strategy

Resume generation uses **Claude API as primary**, with **Gemini as fallback** if `ANTHROPIC_API_KEY` is not set or the call fails:

```python
# app/services/resume_service.py
import os

async def call_llm(system_prompt: str, user_prompt: str) -> str:
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            return await call_claude(system_prompt, user_prompt)
        except Exception as e:
            logger.warning(f"Claude API failed, falling back to Gemini: {e}")
    # Fallback
    return await call_gemini(system_prompt, user_prompt)
```

This means:
- **Now**: `ANTHROPIC_API_KEY` is not yet set → Gemini is used automatically
- **After key is added**: Claude becomes primary, Gemini is fallback on error
- No code changes needed when switching — just add/remove the env variable

---

## Slug Collision Handling

If a slug already exists (same role + company + date), append a counter: `ea-cch-2026-03-23-2`. The `ON CONFLICT (slug) DO UPDATE` in the INSERT handles re-generation of the same resume.

---

## Notes for Implementation

1. **No streaming needed** — generate the full resume in one Claude API call. Expected response time: 10–30 seconds. Set HTTP timeout accordingly.

2. **Token budget** — the prompt will be ~8,000–12,000 tokens. Response ~2,000–3,000 tokens. Use `max_tokens: 4096` for the Claude call.

3. **Error on empty projects** — if the scoring query returns 0 projects, return 400 with `{"error": "No relevant projects found for this vacancy"}` rather than generating an empty resume.

4. **The `source` field** — set to `'bot'` when called from the chatbot, `'manual'` for other callers. This allows filtering in analytics.

5. **Idempotency** — calling the endpoint twice with the same vacancy + same day will update the existing record (via ON CONFLICT). This is intentional.

6. **Bot integration pattern** — the existing chatbot uses WebSocket (`/ws/chat`) in `app/main.py`. Since the resume service lives in the same FastAPI app (Python), the WebSocket handler should call the resume generation logic as an **internal Python function call**, not a separate HTTP request to itself.

   Recommended structure:

```python
# app/services/resume_service.py  ← new file
async def generate_resume(vacancy_text: str, ...) -> dict:
    # Steps 1–8 from this spec
    ...

# app/main.py — in the WebSocket handler (rag_service or main handler):
from app.services.resume_service import generate_resume

# When bot detects resume generation intent:
result = await generate_resume(
    vacancy_text=extracted_vacancy_text,
    role_hint=detected_role,
    # chat_session_id=session_id  # if chat sessions are tracked
)
# Send result back over WebSocket:
await websocket.send_text(result["content_md"])
```

   The REST endpoint `POST /api/resume/generate` is useful for **external callers** (Cowork agent, future automation). Internally the bot calls the function directly.

---

## Implementation Location

Add the following to the existing backend at `digital-avatar/backend/`:

```
digital-avatar/backend/
├── app/
│   ├── main.py                    ← add 3 new routes here (POST/GET/PATCH /api/resume/*)
│   └── services/
│       ├── rag_service.py         ← existing, do not break
│       └── resume_service.py      ← NEW: generate_resume() function + DB helpers
├── requirements.txt               ← add: anthropic>=0.25.0
└── .env                           ← add: ANTHROPIC_API_KEY, RESUME_API_KEY
```

Deployment: same `deploy.sh` flow — no infra changes needed, only new env vars in Cloud Run.

---

## Out of Scope for This Spec

- PDF conversion (future: add `GET /api/resume/:slug/pdf`)
- Resume editing/versioning (future: add `PATCH /api/resume/:slug`)
- GitHub Pages publishing (future: separate push service)
- Authentication beyond API key (future: when multi-user needed)
