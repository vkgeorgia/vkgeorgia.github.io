import hmac
import os
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Header, HTTPException, Query
from fastapi import Path as FastAPIPath

from app import db

router = APIRouter(prefix="/api")


def _check_api_key(x_api_key: Optional[str]) -> None:
    key = os.getenv("CONTACTS_API_KEY", "")
    if key and not hmac.compare_digest(x_api_key or "", key):
        raise HTTPException(status_code=401, detail="Unauthorized")

_CONTACT_FIELDS = ("id", "full_name", "email", "phone", "company", "position", "tags", "notes", "raw_data")


def _row_to_contact(row: Dict[str, Any]) -> Dict[str, Any]:
    return {k: row.get(k) for k in _CONTACT_FIELDS}


@router.get("/contacts")
def api_contacts(
    q: Optional[str] = Query(None),
    x_api_key: Optional[str] = Header(None),
):
    """Return contacts list. Optional q: substring search on full_name / notes."""
    _check_api_key(x_api_key)
    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        if q:
            like = f"%{q}%"
            cur.execute(
                """
                SELECT id, full_name, email, phone, company, position, tags, notes, raw_data
                FROM contacts
                WHERE (full_name ILIKE %s OR notes ILIKE %s)
                ORDER BY full_name NULLS LAST, id ASC
                """,
                (like, like),
            )
        else:
            cur.execute(
                """
                SELECT id, full_name, email, phone, company, position, tags, notes, raw_data
                FROM contacts
                ORDER BY full_name NULLS LAST, id ASC
                """
            )
        rows = cur.fetchall()

    return {"items": [_row_to_contact(r) for r in rows]}


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
            """
            SELECT id, full_name, email, phone, company, position, tags, notes, raw_data
            FROM contacts WHERE id = %s
            """,
            (contact_id,),
        )
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Contact not found")

    return _row_to_contact(row)
