"""Resume generation service.

Steps:
  1. Pre-pass: analyze vacancy text via LLM → structured metadata
  2. Load resume rules from DB
  3. Score and select projects from DB
  4. Load owner profile
  5. Load role summary
  6. Call LLM to generate resume markdown
  7. Save result to generated_resumes table
  8. Return response dict
"""

import json
import logging
import os
import re
from datetime import date
from typing import Optional

import app.db as db

logger = logging.getLogger(__name__)

ROLE_TITLES = {
    "enterprise-architect": "Enterprise Architect",
    "business-analyst": "Business Analyst",
    "project-manager": "Project Manager",
    "consultant": "Consultant",
    "product-manager": "Product Manager",
}

ADJACENT_INDUSTRIES = {
    "finance": ["consulting", "retail"],
    "retail": ["consulting", "manufacturing"],
    "telecom": ["consulting", "manufacturing"],
    "oil-gas": ["manufacturing", "consulting"],
    "aviation": ["consulting", "manufacturing"],
    "healthcare": ["consulting"],
    "manufacturing": ["retail", "consulting"],
    "consulting": ["finance", "telecom", "retail"],
}


# ---------------------------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------------------------

async def _call_claude(system_prompt: str, user_prompt: str) -> str:
    import anthropic
    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    msg = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return msg.content[0].text


async def _call_gemini(system_prompt: str, user_prompt: str) -> str:
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = await model.generate_content_async(f"{system_prompt}\n\n{user_prompt}")
    return response.text


async def _call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call Claude as primary, fall back to Gemini if key absent or call fails."""
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            return await _call_claude(system_prompt, user_prompt)
        except Exception as e:
            logger.warning(f"Claude API failed, falling back to Gemini: {e}")
    return await _call_gemini(system_prompt, user_prompt)


# ---------------------------------------------------------------------------
# Step 1 — Pre-pass: analyze vacancy text
# ---------------------------------------------------------------------------

async def _analyze_vacancy(
    vacancy_text: str,
    role_hint: Optional[str],
    industry_hint: Optional[str],
) -> dict:
    """Extract structured metadata from free-form vacancy text via a small LLM call."""
    system_prompt = (
        "You are a structured data extractor. "
        "Extract information from a job vacancy and return ONLY valid JSON — "
        "no markdown fences, no explanation, no commentary."
    )

    hint_lines = ""
    if role_hint:
        hint_lines += f"\nRole hint from caller: {role_hint}"
    if industry_hint:
        hint_lines += f"\nIndustry hint from caller: {industry_hint}"

    user_prompt = f"""Extract the following fields from the job vacancy text below.
Return ONLY a JSON object with exactly these keys:{hint_lines}

{{
  "target_role": one of [enterprise-architect, business-analyst, project-manager, consultant, product-manager],
  "target_company": company name string or null,
  "target_industry": one of [finance, retail, manufacturing, telecom, oil-gas, aviation, healthcare, consulting] or null,
  "target_domains": array of functional domain keywords found in the text, e.g. ["ERP", "Supply Chain", "TOGAF", "Finance"]
}}

VACANCY TEXT:
{vacancy_text[:3000]}"""

    try:
        raw = await _call_llm(system_prompt, user_prompt)
        raw = re.sub(r"^```[a-z]*\n?", "", raw.strip())
        raw = re.sub(r"\n?```$", "", raw.strip())
        result = json.loads(raw)
        # Normalize: apply hints as fallback if LLM returned null
        if not result.get("target_role") and role_hint:
            result["target_role"] = role_hint
        if not result.get("target_industry") and industry_hint:
            result["target_industry"] = industry_hint
        return result
    except Exception as e:
        logger.warning(f"Vacancy pre-pass failed ({e}), using hints/defaults")
        return {
            "target_role": role_hint or "consultant",
            "target_company": None,
            "target_industry": industry_hint,
            "target_domains": [],
        }


# ---------------------------------------------------------------------------
# Slug helpers
# ---------------------------------------------------------------------------

_ROLE_ABBR = {
    "enterprise-architect": "ea",
    "business-analyst": "ba",
    "project-manager": "pm",
    "consultant": "cons",
    "product-manager": "prod",
}


def _make_slug_base(role: str, company: Optional[str], today: str) -> str:
    abbr = _ROLE_ABBR.get(role, role[:4])
    if company:
        co = re.sub(r"[^a-z0-9]+", "-", company.lower()).strip("-")[:12]
    else:
        co = "general"
    return f"{abbr}-{co}-{today}"


def _resolve_slug(slug_base: str, conn) -> str:
    """Return slug_base, or slug_base-2, slug_base-3 … to avoid collision."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT slug FROM generated_resumes WHERE slug LIKE %s",
            (f"{slug_base}%",),
        )
        existing = {row["slug"] for row in cur.fetchall()}
    if slug_base not in existing:
        return slug_base
    counter = 2
    while f"{slug_base}-{counter}" in existing:
        counter += 1
    return f"{slug_base}-{counter}"


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------

async def generate_resume(
    vacancy_text: str,
    vacancy_url: Optional[str] = None,
    role_hint: Optional[str] = None,
    industry_hint: Optional[str] = None,
    chat_session_id: Optional[str] = None,
    contact_id: Optional[int] = None,
    notes: Optional[str] = None,
    source: str = "manual",
) -> dict:
    today = date.today().isoformat()

    # ------------------------------------------------------------------
    # Step 1 — Pre-pass: extract vacancy metadata
    # ------------------------------------------------------------------
    analysis = await _analyze_vacancy(vacancy_text, role_hint, industry_hint)
    target_role: str = analysis.get("target_role") or "consultant"
    target_company: Optional[str] = analysis.get("target_company")
    target_industry: Optional[str] = analysis.get("target_industry") or industry_hint
    target_domains: list = analysis.get("target_domains") or []

    role_title = ROLE_TITLES.get(target_role, target_role.replace("-", " ").title())
    title = f"{role_title} – {target_company}" if target_company else role_title
    slug_base = _make_slug_base(target_role, target_company, today)

    adjacent = ADJACENT_INDUSTRIES.get(target_industry or "", [])
    domain_like = [f"%{kw}%" for kw in target_domains] if target_domains else ["%"]

    pool = db.get_pool()

    with pool.connection() as conn:
        # --------------------------------------------------------------
        # Step 2 — Load resume rules
        # --------------------------------------------------------------
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT category, rule FROM resume_rules
                WHERE applies_to = 'all'
                   OR applies_to ILIKE %s
                   OR applies_to ILIKE %s
                ORDER BY category, id
                """,
                (f"%{target_role}%", f"%{target_industry or ''}%"),
            )
            rules = cur.fetchall()

        # --------------------------------------------------------------
        # Step 3 — Score and select projects
        # --------------------------------------------------------------
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                  code, title, employer, client, industry, domain, role,
                  year_start, year_end, key_result, executive_md,
                  (
                    CASE WHEN role        ILIKE %s THEN 3 ELSE 0 END +
                    CASE WHEN industry    ILIKE %s THEN 2 ELSE 0 END +
                    CASE WHEN industry    ILIKE ANY(%s) THEN 1 ELSE 0 END +
                    CASE WHEN domain      ILIKE ANY(%s) THEN 2 ELSE 0 END
                  ) AS score
                FROM projects
                WHERE year_end >= (EXTRACT(YEAR FROM NOW()) - 10)
                   OR domain ILIKE ANY(%s)
                ORDER BY score DESC, year_end DESC NULLS LAST
                LIMIT 12
                """,
                (
                    f"%{target_role}%",
                    f"%{target_industry or ''}%",
                    [f"%{a}%" for a in adjacent] or ["%none%"],
                    domain_like,
                    domain_like,
                ),
            )
            projects = cur.fetchall()

        if not projects:
            raise ValueError("No relevant projects found for this vacancy")

        # --------------------------------------------------------------
        # Step 4 — Owner profile
        # --------------------------------------------------------------
        with conn.cursor() as cur:
            cur.execute(
                "SELECT email, linkedin_url, website_url, location, bio "
                "FROM owner_profile WHERE id = 1"
            )
            owner = cur.fetchone() or {}

        # --------------------------------------------------------------
        # Step 5 — Role summary
        # --------------------------------------------------------------
        with conn.cursor() as cur:
            cur.execute(
                "SELECT title, description_md FROM roles WHERE slug = %s",
                (target_role,),
            )
            role_row = cur.fetchone() or {}

        # --------------------------------------------------------------
        # Step 6 — Build prompt and call LLM
        # --------------------------------------------------------------
        rules_text = "\n".join(
            f"{i + 1}. [{r['category']}] {r['rule']}" for i, r in enumerate(rules)
        ) if rules else "(no rules loaded)"

        projects_text = ""
        for p in projects:
            year_end = str(p.get("year_end")) if p.get("year_end") else "present"
            projects_text += (
                f"---\n"
                f"Code: {p.get('code', '')}\n"
                f"Title: {p.get('title', '')}\n"
                f"Client: {p.get('client', '')} | Employer: {p.get('employer', '')}\n"
                f"Industry: {p.get('industry', '')} | Domain: {p.get('domain', '')}\n"
                f"Role: {p.get('role', '')} | Period: {p.get('year_start', '')}–{year_end}\n"
                f"Key result: {p.get('key_result', '')}\n"
                f"Executive description:\n{p.get('executive_md', '')}\n\n"
            )

        system_prompt = (
            "You are a professional resume writer generating tailored resumes for Valerii Korobeinikov. "
            "You must follow ALL rules provided. "
            "Use ONLY the project data provided — do not invent or assume any experience. "
            "Output clean markdown only — no explanations, no comments, no preamble."
        )

        user_prompt = f"""## RULES
{rules_text}

## VACANCY
{vacancy_text}

## EXTRACTED VACANCY ANALYSIS
Role: {target_role}
Industry: {target_industry or 'not specified'}
Key domains: {', '.join(target_domains) if target_domains else 'not specified'}
Company: {target_company or 'not specified'}

## OWNER PROFILE
Email: {owner.get('email', '')}
LinkedIn: {owner.get('linkedin_url', '')}
Location: {owner.get('location', '')}

Bio summary:
{(owner.get('bio') or '')[:500]}

## ROLE SUMMARY (for Summary section framing)
{role_row.get('description_md', '')}

## AVAILABLE PROJECTS (scored by relevance, pick best 6-8)
{projects_text}
## TASK
Generate a complete, tailored resume in markdown format for the vacancy above.
Apply all rules. Select 6-8 most relevant projects.
Return ONLY the markdown — no commentary before or after."""

        content_md = await _call_llm(system_prompt, user_prompt)

        # --------------------------------------------------------------
        # Step 7 — Save to DB
        # --------------------------------------------------------------
        slug = _resolve_slug(slug_base, conn)

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO generated_resumes (
                  slug, title, target_role, target_company, target_industry,
                  vacancy_text, vacancy_url, content_md,
                  status, source, chat_session_id, contact_id, notes
                ) VALUES (
                  %s, %s, %s, %s, %s,
                  %s, %s, %s,
                  'ready', %s, %s, %s, %s
                )
                ON CONFLICT (slug) DO UPDATE
                  SET content_md = EXCLUDED.content_md,
                      status     = 'ready',
                      updated_at = now()
                RETURNING id, slug, title, content_md, created_at
                """,
                (
                    slug, title, target_role, target_company, target_industry,
                    vacancy_text, vacancy_url, content_md,
                    source, chat_session_id, contact_id, notes,
                ),
            )
            row = cur.fetchone()

    # Step 8 — Return
    return {
        "id": str(row["id"]),
        "slug": row["slug"],
        "title": row["title"],
        "content_md": row["content_md"],
        "created_at": row["created_at"].isoformat(),
    }
