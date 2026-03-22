from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi import Path as FastAPIPath

from app import db

router = APIRouter(prefix="/api")

_CONTACT_FIELDS = ("id", "full_name", "email", "phone", "company", "position", "tags", "notes", "raw_data")


def _row_to_contact(row: Dict[str, Any]) -> Dict[str, Any]:
    return {k: row.get(k) for k in _CONTACT_FIELDS}


@router.get("/contacts")
def api_contacts(q: Optional[str] = Query(None)):
    """Return contacts list. Optional q: substring search on full_name / notes."""
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
def api_contact_detail(contact_id: int = FastAPIPath(..., ge=1)):
    """Return single contact by id."""
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
