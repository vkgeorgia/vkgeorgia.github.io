"""
PATCH для digital-avatar/backend/app/routers/contacts.py
Заменить ВЕСЬ файл этим содержимым.

Изменения:
  - Добавлен POST /api/contacts  — создание лида из чата
  - Добавлен PATCH /api/contacts/{id} — обновление статуса/данных
  - GET-эндпоинты расширены новыми полями (source, status, created_at и др.)
"""

import hmac
import os
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Header, HTTPException, Query
from fastapi import Path as FastAPIPath
from pydantic import BaseModel

from app import db

router = APIRouter(prefix="/api")


def _check_api_key(x_api_key: Optional[str]) -> None:
    key = os.getenv("CONTACTS_API_KEY", "")
    if key and not hmac.compare_digest(x_api_key or "", key):
        raise HTTPException(status_code=401, detail="Unauthorized")


_CONTACT_FIELDS = (
    "id", "full_name", "email", "phone", "company", "position",
    "tags", "notes", "raw_data", "country",
    "source", "status", "chat_session_id", "lead_score",
    "linkedin_url", "created_at", "updated_at",
)


def _row_to_contact(row: Dict[str, Any]) -> Dict[str, Any]:
    result = {k: row.get(k) for k in _CONTACT_FIELDS}
    # Serialize non-serializable types
    if result.get("created_at"):
        result["created_at"] = result["created_at"].isoformat()
    if result.get("updated_at"):
        result["updated_at"] = result["updated_at"].isoformat()
    if result.get("chat_session_id"):
        result["chat_session_id"] = str(result["chat_session_id"])
    return result


# --------------------------------------------------------------------------- #
# Pydantic models                                                               #
# --------------------------------------------------------------------------- #

class ContactCreate(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    source: str = "chatbot"
    status: str = "lead"
    chat_session_id: Optional[str] = None
    lead_score: int = 10


class ContactUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    status: Optional[str] = None
    lead_score: Optional[int] = None


# --------------------------------------------------------------------------- #
# GET /api/contacts                                                             #
# --------------------------------------------------------------------------- #

@router.get("/contacts")
def api_contacts(
    q: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    x_api_key: Optional[str] = Header(None),
):
    """Return contacts list. Optional filters: q (search), status, source."""
    _check_api_key(x_api_key)
    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        conditions = []
        params = []

        if q:
            conditions.append("(full_name ILIKE %s OR notes ILIKE %s OR email ILIKE %s)")
            like = f"%{q}%"
            params.extend([like, like, like])
        if status:
            conditions.append("status = %s")
            params.append(status)
        if source:
            conditions.append("source = %s")
            params.append(source)

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        cur.execute(
            f"""
            SELECT {", ".join(_CONTACT_FIELDS)}
            FROM contacts
            {where}
            ORDER BY created_at DESC NULLS LAST, full_name NULLS LAST, id ASC
            """,
            params,
        )
        rows = cur.fetchall()
    return {"items": [_row_to_contact(r) for r in rows], "total": len(rows)}


# --------------------------------------------------------------------------- #
# GET /api/contacts/{id}                                                        #
# --------------------------------------------------------------------------- #

@router.get("/contacts/{contact_id}")
def api_contact_detail(
    contact_id: int = FastAPIPath(..., ge=1),
    x_api_key: Optional[str] = Header(None),
):
    """Return single contact by id."""
    _check_api_key(x_api_key)
    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        cur.execute(
            f"SELECT {', '.join(_CONTACT_FIELDS)} FROM contacts WHERE id = %s",
            (contact_id,),
        )
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Contact not found")
    return _row_to_contact(row)


# --------------------------------------------------------------------------- #
# POST /api/contacts  — called by chatbot when user shares contact info        #
# --------------------------------------------------------------------------- #

@router.post("/contacts", status_code=201)
def api_create_contact(
    body: ContactCreate,
    x_api_key: Optional[str] = Header(None),
):
    """Create a new contact / lead. Called by chatbot on lead capture."""
    _check_api_key(x_api_key)

    with db.get_pool().connection() as conn:
        cur = conn.cursor()

        # Avoid exact duplicates by email
        if body.email:
            cur.execute("SELECT id FROM contacts WHERE email = %s", (body.email,))
            existing = cur.fetchone()
            if existing:
                # Update existing contact with chatbot data
                cur.execute(
                    """
                    UPDATE contacts SET
                        status = CASE WHEN status = 'contact' THEN %s ELSE status END,
                        chat_session_id = COALESCE(chat_session_id, %s::uuid),
                        notes = COALESCE(notes || E'\n---\n' || %s, notes, %s),
                        updated_at = NOW()
                    WHERE id = %s
                    RETURNING id
                    """,
                    (
                        body.status,
                        body.chat_session_id,
                        body.notes,
                        body.notes,
                        existing["id"],
                    ),
                )
                conn.commit()
                return {"id": existing["id"], "action": "updated"}

        cur.execute(
            """
            INSERT INTO contacts
              (full_name, email, phone, company, position, tags, notes,
               country, linkedin_url, source, status, chat_session_id, lead_score)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::uuid,%s)
            RETURNING id
            """,
            (
                body.full_name, body.email, body.phone, body.company,
                body.position, body.tags, body.notes, body.country,
                body.linkedin_url, body.source, body.status,
                body.chat_session_id, body.lead_score,
            ),
        )
        row = cur.fetchone()
        conn.commit()
    return {"id": row["id"], "action": "created"}


# --------------------------------------------------------------------------- #
# PATCH /api/contacts/{id}                                                     #
# --------------------------------------------------------------------------- #

@router.patch("/contacts/{contact_id}")
def api_update_contact(
    body: ContactUpdate,
    contact_id: int = FastAPIPath(..., ge=1),
    x_api_key: Optional[str] = Header(None),
):
    """Update contact fields and/or status."""
    _check_api_key(x_api_key)

    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    values = list(updates.values()) + [contact_id]

    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        cur.execute(
            f"UPDATE contacts SET {set_clause}, updated_at = NOW() WHERE id = %s RETURNING id",
            values,
        )
        row = cur.fetchone()
        conn.commit()

    if not row:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"id": row["id"], "action": "updated"}
