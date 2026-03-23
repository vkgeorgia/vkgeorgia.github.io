#!/usr/bin/env python3
"""
Generate embeddings for all knowledge chunks and store in Neon (pgvector).

Usage:
    GEMINI_API_KEY=xxx NEON_DATABASE_URL=xxx python scripts/generate_embeddings.py

Reads GEMINI_API_KEY and NEON_DATABASE_URL from environment (or backend/.env).
Chunks projects and knowledge-base files, generates embeddings via Gemini
text-embedding-004 (768 dims), upserts into knowledge_chunks table.

Run this script after generate_kb.py on each deploy.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "digital-avatar" / "backend"
KB_DIR = REPO_ROOT / "knowledge-base"

# Load .env from backend if keys not already set
def _load_env():
    env_file = BACKEND_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

_load_env()

DB_URL = os.getenv("NEON_DATABASE_URL")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not DB_URL:
    print("ERROR: NEON_DATABASE_URL not set", file=sys.stderr)
    sys.exit(1)
if not GEMINI_KEY:
    print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
    sys.exit(1)

import json
import urllib.request

try:
    import psycopg
except ImportError:
    print("ERROR: psycopg not installed. Run: pip install psycopg psycopg[binary]", file=sys.stderr)
    sys.exit(1)

_EMBED_URL = (
    f"https://generativelanguage.googleapis.com/v1/models/"
    f"text-embedding-004:batchEmbedContents?key={GEMINI_KEY}"
)

# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

MAX_CHUNK_CHARS = 2000  # ~500 tokens, safe for embedding model


def _chunks_from_text(text: str, source: str) -> List[Tuple[str, str, int]]:
    """Split text into chunks. Returns list of (source, content, index)."""
    text = text.strip()
    if not text:
        return []
    # Split on double newlines first (paragraph boundaries)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 <= MAX_CHUNK_CHARS:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append(current)
            # If single para is too long, hard-split it
            while len(para) > MAX_CHUNK_CHARS:
                chunks.append(para[:MAX_CHUNK_CHARS])
                para = para[MAX_CHUNK_CHARS:]
            current = para
    if current:
        chunks.append(current)
    return [(source, c, i) for i, c in enumerate(chunks)]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_project_chunks(conn) -> List[Tuple[str, str, int]]:
    """One rich-text chunk per project from DB."""
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.code, p.title, p.employer, p.client,
               p.industry, p.domain, p.role, p.year_start, p.year_end,
               p.technology, p.star_situation, p.star_task, p.star_action,
               p.star_result, p.key_result, p.executive_md
        FROM projects p ORDER BY p.num_legacy
    """)
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]

    cur.execute("SELECT project_id, slug FROM project_domains")
    dm = {}
    for pid, s in cur.fetchall():
        dm.setdefault(pid, []).append(s)

    cur.execute("SELECT project_id, slug FROM project_industries")
    im = {}
    for pid, s in cur.fetchall():
        im.setdefault(pid, []).append(s)

    cur.execute("SELECT project_id, slug FROM project_roles")
    rm = {}
    for pid, s in cur.fetchall():
        rm.setdefault(pid, []).append(s)

    all_chunks = []
    for p in rows:
        pid = p["id"]
        period = str(p.get("year_start") or "?")
        if p.get("year_end") and p["year_end"] != p.get("year_start"):
            period += f"–{p['year_end']}"
        parts = [
            f"Project: {p['title']} ({p['code']})",
            f"Period: {period} | Role: {p.get('role') or '—'}",
            f"Employer: {p.get('employer') or '—'} | Client: {p.get('client') or '—'}",
            f"Industry: {p.get('industry') or '—'} | Domain: {p.get('domain') or '—'}",
        ]
        if dm.get(pid):
            parts.append(f"Domain tags: {', '.join(dm[pid])}")
        if im.get(pid):
            parts.append(f"Industry tags: {', '.join(im[pid])}")
        if rm.get(pid):
            parts.append(f"Role tags: {', '.join(rm[pid])}")
        if p.get("technology"):
            parts.append(f"Technologies: {p['technology']}")
        if p.get("key_result"):
            parts.append(f"\nKey Result: {p['key_result']}")
        if p.get("executive_md"):
            parts.append(f"\n{p['executive_md'].strip()}")
        else:
            for field in ["star_situation", "star_task", "star_action", "star_result"]:
                if p.get(field):
                    label = field.replace("star_", "").title()
                    parts.append(f"\n{label}: {p[field].strip()}")

        text = "\n".join(parts)
        source = f"project:{p['code']}"
        all_chunks.extend(_chunks_from_text(text, source))

    return all_chunks


def load_kb_file_chunks() -> List[Tuple[str, str, int]]:
    """Chunk all .md/.txt files from knowledge-base (excluding sources/ dirs)."""
    all_chunks = []
    for pattern in ["*.md", "*.txt"]:
        for f in KB_DIR.rglob(pattern):
            if "sources" in f.parts:
                continue
            try:
                text = f.read_text(encoding="utf-8").strip()
                # Strip YAML frontmatter
                if text.startswith("---"):
                    end = text.find("---", 3)
                    if end != -1:
                        text = text[end + 3:].strip()
                if not text:
                    continue
                source = f"file:{f.relative_to(REPO_ROOT)}"
                all_chunks.extend(_chunks_from_text(text, source))
            except Exception as e:
                print(f"  WARNING: could not read {f}: {e}")
    return all_chunks


# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------

BATCH_SIZE = 100  # Gemini allows up to 100 texts per batch call
RETRY_DELAY = 5   # seconds between retries on rate limit


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Embed a batch of texts via Gemini REST API (v1). Returns list of 768-dim vectors."""
    payload = json.dumps({
        "requests": [
            {
                "model": "models/text-embedding-004",
                "content": {"parts": [{"text": t}]},
                "taskType": "RETRIEVAL_DOCUMENT",
            }
            for t in texts
        ]
    }).encode()
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                _EMBED_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
            return [e["values"] for e in data["embeddings"]]
        except Exception as e:
            if attempt < 2:
                print(f"  Embedding error (attempt {attempt+1}): {e}. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY * (attempt + 1))
            else:
                raise


# ---------------------------------------------------------------------------
# Upsert
# ---------------------------------------------------------------------------

def upsert_chunks(conn, chunks_with_embeddings):
    """Upsert (source, chunk_index, content, embedding) into knowledge_chunks."""
    cur = conn.cursor()
    upserted = 0
    for source, chunk_index, content, embedding in chunks_with_embeddings:
        cur.execute("""
            INSERT INTO knowledge_chunks (source, chunk_index, content, embedding)
            VALUES (%s, %s, %s, %s::vector)
            ON CONFLICT (source, chunk_index) DO UPDATE
              SET content = EXCLUDED.content,
                  embedding = EXCLUDED.embedding,
                  created_at = NOW()
        """, (source, chunk_index, content, str(embedding)))
        upserted += 1
    conn.commit()
    return upserted


def delete_stale_chunks(conn, current_sources: set):
    """Remove chunks for sources no longer present."""
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT source FROM knowledge_chunks")
    db_sources = {r[0] for r in cur.fetchall()}
    stale = db_sources - current_sources
    if stale:
        for s in stale:
            cur.execute("DELETE FROM knowledge_chunks WHERE source = %s", (s,))
        conn.commit()
        print(f"  Deleted stale chunks for {len(stale)} sources: {sorted(stale)[:5]}{'...' if len(stale)>5 else ''}")
    return len(stale)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Connecting to DB...")
    conn = psycopg.connect(DB_URL)

    print("Loading project chunks from DB...")
    project_chunks = load_project_chunks(conn)
    print(f"  {len(project_chunks)} project chunks")

    print("Loading knowledge-base file chunks...")
    kb_chunks = load_kb_file_chunks()
    print(f"  {len(kb_chunks)} file chunks")

    all_chunks = project_chunks + kb_chunks
    print(f"Total: {len(all_chunks)} chunks\n")

    current_sources = {c[0] for c in all_chunks}

    # Generate embeddings in batches
    print("Generating embeddings...")
    texts = [c[1] for c in all_chunks]
    all_embeddings = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        print(f"  Batch {i // BATCH_SIZE + 1}/{(len(texts) + BATCH_SIZE - 1) // BATCH_SIZE} ({len(batch)} texts)...", end=" ", flush=True)
        embeddings = embed_batch(batch)
        all_embeddings.extend(embeddings)
        print("done")
        if i + BATCH_SIZE < len(texts):
            time.sleep(0.5)  # gentle rate limiting

    # Upsert
    print("\nUpserting into knowledge_chunks...")
    chunks_with_embeddings = [
        (all_chunks[i][0], all_chunks[i][2], all_chunks[i][1], all_embeddings[i])
        for i in range(len(all_chunks))
    ]
    n = upsert_chunks(conn, chunks_with_embeddings)
    print(f"  Upserted {n} chunks")

    # Clean up stale
    delete_stale_chunks(conn, current_sources)

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
