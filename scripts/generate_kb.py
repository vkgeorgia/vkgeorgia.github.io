#!/usr/bin/env python3
"""
Generate knowledge-base summary files from Neon DB.

Usage:
    python scripts/generate_kb.py

Reads NEON_DATABASE_URL from environment (or `.env` in repo root, then `digital-avatar/backend/.env`).
Writes/updates files in knowledge-base/domains/, knowledge-base/industries/,
knowledge-base/roles/.

Run this script whenever projects data in DB is updated.
Can also be triggered as part of CI/CD or a cron job.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Allow running from repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "digital-avatar" / "backend"
KB_DIR = REPO_ROOT / "knowledge-base"

def _merge_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))


# Корневой .env имеет приоритет над legacy backend/.env (setdefault: первый выигрывает)
for _env_path in (REPO_ROOT / ".env", BACKEND_DIR / ".env"):
    _merge_dotenv(_env_path)

DB_URL = os.getenv("NEON_DATABASE_URL")
if not DB_URL:
    print("ERROR: NEON_DATABASE_URL not set", file=sys.stderr)
    sys.exit(1)

try:
    import psycopg
except ImportError:
    print("ERROR: psycopg not installed. Run: pip install psycopg psycopg[binary]", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def load_data(conn) -> dict:
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.id, p.code, p.title, p.employer, p.client,
            p.industry, p.domain, p.role,
            p.year_start, p.year_end,
            p.technology,
            p.star_situation, p.star_task, p.star_action, p.star_result,
            p.key_result, p.executive_md
        FROM projects p
        ORDER BY p.year_start DESC NULLS LAST, p.id
    """)
    cols = [d[0] for d in cur.description]
    projects = [dict(zip(cols, row)) for row in cur.fetchall()]

    cur.execute("SELECT project_id, slug FROM project_domains")
    domain_map: dict = {}
    for pid, slug in cur.fetchall():
        domain_map.setdefault(pid, []).append(slug)

    cur.execute("SELECT project_id, slug FROM project_industries")
    industry_map: dict = {}
    for pid, slug in cur.fetchall():
        industry_map.setdefault(pid, []).append(slug)

    cur.execute("SELECT project_id, slug FROM project_roles")
    role_map: dict = {}
    for pid, slug in cur.fetchall():
        role_map.setdefault(pid, []).append(slug)

    return {
        "projects": projects,
        "domain_map": domain_map,
        "industry_map": industry_map,
        "role_map": role_map,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Acronyms to keep uppercase in generated titles
_UPPER_WORDS = {"ai", "iot", "bim", "erp", "scm", "crm", "hr", "pm", "bi", "poc"}


def _slug_to_title(slug: str) -> str:
    """Convert a slug like 'ai-consulting' → 'AI Consulting'."""
    parts = slug.replace("-", " ").split()
    return " ".join(w.upper() if w.lower() in _UPPER_WORDS else w.title() for w in parts)


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def _project_block(p: dict, domain_tags: list, industry_tags: list, role_tags: list) -> str:
    lines = []
    period = str(p.get("year_start") or "?")
    if p.get("year_end") and p["year_end"] != p.get("year_start"):
        period += f"–{p['year_end']}"

    lines.append(f"### {p['title']} ({p['code']})")
    lines.append(f"- **Period:** {period}")
    lines.append(f"- **Role:** {p.get('role') or '—'}")
    lines.append(f"- **Employer:** {p.get('employer') or '—'}")
    lines.append(f"- **Client:** {p.get('client') or '—'}")
    lines.append(f"- **Industry:** {p.get('industry') or '—'}")
    lines.append(f"- **Domain:** {p.get('domain') or '—'}")
    if p.get("technology"):
        lines.append(f"- **Technologies:** {p['technology']}")
    if domain_tags:
        lines.append(f"- **Domain tags:** {', '.join(domain_tags)}")
    if industry_tags:
        lines.append(f"- **Industry tags:** {', '.join(industry_tags)}")
    if role_tags:
        lines.append(f"- **Role tags:** {', '.join(role_tags)}")

    if p.get("key_result"):
        lines.append(f"\n**Key Result:** {p['key_result']}")

    if p.get("executive_md"):
        lines.append(f"\n{p['executive_md'].strip()}")
    else:
        if p.get("star_situation"):
            lines.append(f"\n**Situation:** {p['star_situation'].strip()}")
        if p.get("star_result"):
            lines.append(f"\n**Result:** {p['star_result'].strip()}")

    return "\n".join(lines)


def _write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def generate_domain_files(data: dict) -> int:
    projects = data["projects"]
    domain_map = data["domain_map"]
    industry_map = data["industry_map"]
    role_map = data["role_map"]

    # Group projects by domain slug
    slug_to_projects: dict = {}
    for p in projects:
        pid = p["id"]
        for slug in domain_map.get(pid, []):
            slug_to_projects.setdefault(slug, []).append(p)

    written = 0
    for slug, slug_projects in sorted(slug_to_projects.items()):
        title = _slug_to_title(slug)
        lines = [f"# {title} — Projects by Domain\n"]
        lines.append(f"Domain tag: `{slug}`  ")
        lines.append(f"Projects: {len(slug_projects)}\n")

        for p in slug_projects:
            pid = p["id"]
            lines.append(_project_block(
                p,
                domain_map.get(pid, []),
                industry_map.get(pid, []),
                role_map.get(pid, []),
            ))
            lines.append("")

        content = "\n".join(lines)
        path = KB_DIR / "domains" / f"{slug}.md"
        changed = _write_if_changed(path, content)
        if changed:
            written += 1
            print(f"  [domain] wrote {path.relative_to(REPO_ROOT)}")

    return written


def generate_industry_files(data: dict) -> int:
    projects = data["projects"]
    domain_map = data["domain_map"]
    industry_map = data["industry_map"]
    role_map = data["role_map"]

    slug_to_projects: dict = {}
    for p in projects:
        pid = p["id"]
        for slug in industry_map.get(pid, []):
            slug_to_projects.setdefault(slug, []).append(p)

    written = 0
    for slug, slug_projects in sorted(slug_to_projects.items()):
        title = _slug_to_title(slug)
        lines = [f"# {title} — Projects by Industry\n"]
        lines.append(f"Industry tag: `{slug}`  ")
        lines.append(f"Projects: {len(slug_projects)}\n")

        for p in slug_projects:
            pid = p["id"]
            lines.append(_project_block(
                p,
                domain_map.get(pid, []),
                industry_map.get(pid, []),
                role_map.get(pid, []),
            ))
            lines.append("")

        content = "\n".join(lines)
        path = KB_DIR / "industries" / f"{slug}.md"
        changed = _write_if_changed(path, content)
        if changed:
            written += 1
            print(f"  [industry] wrote {path.relative_to(REPO_ROOT)}")

    return written


def generate_role_files(data: dict) -> int:
    projects = data["projects"]
    domain_map = data["domain_map"]
    industry_map = data["industry_map"]
    role_map = data["role_map"]

    slug_to_projects: dict = {}
    for p in projects:
        pid = p["id"]
        for slug in role_map.get(pid, []):
            slug_to_projects.setdefault(slug, []).append(p)

    written = 0
    for slug, slug_projects in sorted(slug_to_projects.items()):
        title = _slug_to_title(slug)
        lines = [f"# {title} — Projects by Role\n"]
        lines.append(f"Role tag: `{slug}`  ")
        lines.append(f"Projects: {len(slug_projects)}\n")

        for p in slug_projects:
            pid = p["id"]
            lines.append(_project_block(
                p,
                domain_map.get(pid, []),
                industry_map.get(pid, []),
                role_map.get(pid, []),
            ))
            lines.append("")

        content = "\n".join(lines)
        path = KB_DIR / "roles" / f"{slug}.md"
        changed = _write_if_changed(path, content)
        if changed:
            written += 1
            print(f"  [role] wrote {path.relative_to(REPO_ROOT)}")

    return written


def generate_all_projects_index(data: dict) -> int:
    """Single file with all projects — useful as a catch-all for RAG."""
    projects = data["projects"]
    domain_map = data["domain_map"]
    industry_map = data["industry_map"]
    role_map = data["role_map"]

    lines = [f"# All Projects — Full Index\n"]
    lines.append(f"Total: {len(projects)} projects\n")

    for p in projects:
        pid = p["id"]
        lines.append(_project_block(
            p,
            domain_map.get(pid, []),
            industry_map.get(pid, []),
            role_map.get(pid, []),
        ))
        lines.append("")

    content = "\n".join(lines)
    path = KB_DIR / "projects" / "all-projects.md"
    changed = _write_if_changed(path, content)
    if changed:
        print(f"  [all] wrote {path.relative_to(REPO_ROOT)}")
        return 1
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Connecting to DB...")
    conn = psycopg.connect(DB_URL)
    print(f"Loading data...")
    data = load_data(conn)
    conn.close()

    n_projects = len(data["projects"])
    print(f"Loaded {n_projects} projects from DB\n")

    total = 0
    total += generate_domain_files(data)
    total += generate_industry_files(data)
    total += generate_role_files(data)
    total += generate_all_projects_index(data)

    print(f"\nDone. {total} files written/updated.")


if __name__ == "__main__":
    main()
