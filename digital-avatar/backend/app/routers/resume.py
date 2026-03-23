import logging
import os
from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

import app.db as db
from app.services.resume_service import generate_resume

logger = logging.getLogger(__name__)
router = APIRouter()


def _check_api_key(x_api_key: Optional[str]) -> None:
    key = os.getenv("RESUME_API_KEY", "")
    if key and x_api_key != key:
        raise HTTPException(status_code=401, detail="Unauthorized")


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    vacancy_text: str
    vacancy_url: Optional[str] = None
    role_hint: Optional[str] = None
    industry_hint: Optional[str] = None
    chat_session_id: Optional[str] = None
    contact_id: Optional[int] = None
    notes: Optional[str] = None


class StatusUpdateRequest(BaseModel):
    status: str
    sent_to: Optional[str] = None
    sent_at: Optional[str] = None


# ---------------------------------------------------------------------------
# POST /api/resume/generate
# ---------------------------------------------------------------------------

@router.post("/api/resume/generate")
async def resume_generate(
    body: GenerateRequest,
    x_api_key: Optional[str] = Header(default=None),
):
    _check_api_key(x_api_key)

    if not body.vacancy_text or not body.vacancy_text.strip():
        raise HTTPException(status_code=400, detail="vacancy_text is required")

    try:
        result = await generate_resume(
            vacancy_text=body.vacancy_text,
            vacancy_url=body.vacancy_url,
            role_hint=body.role_hint,
            industry_hint=body.industry_hint,
            chat_session_id=body.chat_session_id,
            contact_id=body.contact_id,
            notes=body.notes,
            source="bot" if body.chat_session_id else "manual",
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Resume generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "Generation failed", "detail": str(e)},
        )


# ---------------------------------------------------------------------------
# GET /api/resume/{slug}
# ---------------------------------------------------------------------------

@router.get("/api/resume/{slug}")
async def resume_get(
    slug: str,
    x_api_key: Optional[str] = Header(default=None),
):
    _check_api_key(x_api_key)

    with db.get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, slug, title, content_md,
                       target_role, target_company, target_industry,
                       status, created_at
                FROM generated_resumes
                WHERE slug = %s
                """,
                (slug,),
            )
            row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Resume not found")

    return {
        "id": str(row["id"]),
        "slug": row["slug"],
        "title": row["title"],
        "content_md": row["content_md"],
        "target_role": row.get("target_role"),
        "target_company": row.get("target_company"),
        "target_industry": row.get("target_industry"),
        "status": row["status"],
        "created_at": row["created_at"].isoformat(),
    }


# ---------------------------------------------------------------------------
# PATCH /api/resume/{slug}/status
# ---------------------------------------------------------------------------

@router.patch("/api/resume/{slug}/status")
async def resume_update_status(
    slug: str,
    body: StatusUpdateRequest,
    x_api_key: Optional[str] = Header(default=None),
):
    _check_api_key(x_api_key)

    valid_statuses = {"draft", "ready", "sent", "viewed"}
    if body.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"status must be one of: {', '.join(sorted(valid_statuses))}",
        )

    with db.get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE generated_resumes
                SET status     = %s,
                    sent_to    = COALESCE(%s, sent_to),
                    sent_at    = COALESCE(%s::timestamptz, sent_at),
                    updated_at = now()
                WHERE slug = %s
                RETURNING slug
                """,
                (body.status, body.sent_to, body.sent_at, slug),
            )
            row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Resume not found")

    return {"slug": row["slug"], "status": body.status}
