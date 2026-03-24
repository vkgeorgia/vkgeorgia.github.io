import hmac
import os
from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from fastapi import Path as FastAPIPath
from pydantic import BaseModel

from app import db
from app.services.resume_service import _call_llm

router = APIRouter(prefix="/api")


def _check_api_key(x_api_key: Optional[str]) -> None:
    key = os.getenv("CONTACTS_API_KEY", "")
    if key and not hmac.compare_digest(x_api_key or "", key):
        raise HTTPException(status_code=401, detail="Unauthorized")


# --------------------------------------------------------------------------- #
# Pydantic models                                                               #
# --------------------------------------------------------------------------- #

class ProposalCreate(BaseModel):
    contact_id: Optional[int] = None
    chat_session_id: Optional[str] = None
    title: str
    vacancy_text: Optional[str] = None
    context: Optional[str] = None   # extra context from user


class ProposalUpdate(BaseModel):
    status: Optional[str] = None    # draft, sent, accepted, rejected
    title: Optional[str] = None
    content_md: Optional[str] = None


# --------------------------------------------------------------------------- #
# GET /api/proposals                                                            #
# --------------------------------------------------------------------------- #

@router.get("/proposals")
def api_list_proposals(
    x_api_key: Optional[str] = Header(None),
):
    _check_api_key(x_api_key)
    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.id, p.title, p.status, p.created_at, p.updated_at,
                   c.full_name as contact_name, c.company as contact_company
            FROM proposals p
            LEFT JOIN contacts c ON c.id = p.contact_id
            ORDER BY p.created_at DESC
            """
        )
        rows = cur.fetchall()
    return {
        "items": [
            {
                "id": r["id"],
                "title": r["title"],
                "status": r["status"],
                "contact_name": r["contact_name"],
                "contact_company": r["contact_company"],
                "created_at": r["created_at"].isoformat() if r["created_at"] else None,
                "updated_at": r["updated_at"].isoformat() if r["updated_at"] else None,
            }
            for r in rows
        ]
    }


# --------------------------------------------------------------------------- #
# GET /api/proposals/{id}                                                       #
# --------------------------------------------------------------------------- #

@router.get("/proposals/{proposal_id}")
def api_get_proposal(
    proposal_id: int = FastAPIPath(..., ge=1),
    x_api_key: Optional[str] = Header(None),
):
    _check_api_key(x_api_key)
    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.*, c.full_name as contact_name, c.email as contact_email
            FROM proposals p
            LEFT JOIN contacts c ON c.id = p.contact_id
            WHERE p.id = %s
            """,
            (proposal_id,),
        )
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return dict(row)


# --------------------------------------------------------------------------- #
# POST /api/proposals  — generate commercial proposal via AI                   #
# --------------------------------------------------------------------------- #

@router.post("/proposals", status_code=201)
async def api_create_proposal(
    body: ProposalCreate,
    x_api_key: Optional[str] = Header(None),
):
    """Generate a commercial proposal (КП) using AI and save to DB."""
    _check_api_key(x_api_key)

    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT bio, raw_data FROM owner_profile LIMIT 1")
        profile = cur.fetchone()

        cur.execute(
            """
            SELECT title, role, industry, domain, star_result, key_result,
                   year_start, year_end, technology
            FROM projects
            ORDER BY year_end DESC NULLS FIRST
            LIMIT 15
            """
        )
        projects = cur.fetchall()

        contact_info = ""
        if body.contact_id:
            cur.execute(
                "SELECT full_name, company, position FROM contacts WHERE id = %s",
                (body.contact_id,),
            )
            contact = cur.fetchone()
            if contact:
                contact_info = (
                    f"Client: {contact['full_name']}, "
                    f"{contact['position'] or ''} at {contact['company'] or ''}"
                )

    profile_bio = profile["bio"] if profile else ""
    projects_text = "\n".join(
        f"- {p['year_start']}-{p['year_end']}: {p['title']} ({p['role']}, {p['industry']}) — {p['key_result'] or p['star_result'] or ''}"
        for p in projects
    )

    system_prompt = """You are a business development expert helping create compelling commercial proposals.
Write a professional commercial proposal in the same language as the client's request.
Structure: Executive Summary → Understanding of Client Needs → Our Approach → Relevant Experience → Proposed Solution → Why Us → Next Steps.
Be specific, results-focused, and professional. Use the provided experience and context."""

    user_prompt = f"""Create a commercial proposal for the following:

CLIENT: {contact_info or 'Prospective client'}
TITLE: {body.title}

CLIENT'S NEEDS / VACANCY:
{body.vacancy_text or body.context or 'General consulting engagement'}

CONSULTANT PROFILE:
{profile_bio}

RELEVANT EXPERIENCE:
{projects_text}

Generate a compelling commercial proposal in Markdown format."""

    content_md = await _call_llm(system_prompt, user_prompt)

    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO proposals
              (contact_id, chat_session_id, title, content_md, status, vacancy_text)
            VALUES (%s, %s::uuid, %s, %s, 'draft', %s)
            RETURNING id
            """,
            (
                body.contact_id,
                body.chat_session_id,
                body.title,
                content_md,
                body.vacancy_text or body.context,
            ),
        )
        row = cur.fetchone()
        conn.commit()

    return {"id": row["id"], "content_md": content_md, "status": "draft"}


# --------------------------------------------------------------------------- #
# PATCH /api/proposals/{id}                                                    #
# --------------------------------------------------------------------------- #

@router.patch("/proposals/{proposal_id}")
def api_update_proposal(
    body: ProposalUpdate,
    proposal_id: int = FastAPIPath(..., ge=1),
    x_api_key: Optional[str] = Header(None),
):
    _check_api_key(x_api_key)
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    values = list(updates.values()) + [proposal_id]

    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        cur.execute(
            f"UPDATE proposals SET {set_clause}, updated_at = NOW() WHERE id = %s RETURNING id",
            values,
        )
        row = cur.fetchone()
        conn.commit()

    if not row:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return {"id": row["id"], "action": "updated"}
