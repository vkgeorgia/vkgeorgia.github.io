import os
from typing import Optional

from fastapi import APIRouter, Header, HTTPException

from app import db, telegram_notify

router = APIRouter()

VERSION = "router-split-pool-history-v5"


@router.get("/")
async def root():
    return {"message": "Digital Avatar Backend is running", "version": VERSION}


@router.get("/api/health")
def api_health():
    db_ok = False
    try:
        with db.get_pool().connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        db_ok = True
    except Exception:
        pass

    return {
        "ok": True,
        "version": VERSION,
        "db": {"ok": db_ok},
        "telegram": telegram_notify.diagnostics(),
    }


@router.post("/api/internal/telegram-test")
def api_telegram_test(authorization: Optional[str] = Header(None, alias="Authorization")):
    """
    Manual Telegram delivery test. Protected by TELEGRAM_DIAG_SECRET env var.
    Pass: Authorization: Bearer <secret>
    Returns 404 if secret is not configured (endpoint is hidden).
    """
    secret = os.getenv("TELEGRAM_DIAG_SECRET", "").strip()
    if not secret:
        raise HTTPException(status_code=404, detail="Not Found")
    if (authorization or "").strip() != f"Bearer {secret}":
        raise HTTPException(status_code=403, detail="Forbidden")
    return telegram_notify.send_test_message()
