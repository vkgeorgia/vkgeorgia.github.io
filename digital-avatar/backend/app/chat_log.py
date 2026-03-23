"""
Persist WebSocket chat turns to Neon (PostgreSQL).

Requires tables from sql/chat_logs.sql. If inserts fail, errors are logged
and the chat flow continues (best-effort logging).
"""
from __future__ import annotations

import json
import logging
import uuid
from typing import Any, Dict, Optional

from app.db import get_pool

logger = logging.getLogger(__name__)


def create_session(
    client_ip: Optional[str] = None,
    user_agent: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> Optional[str]:
    """Create a chat_sessions row; returns session UUID string or None on failure."""
    sid = str(uuid.uuid4())
    try:
        with get_pool().connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO chat_sessions (id, client_ip, user_agent, meta)
                    VALUES (%s, %s, %s, %s::jsonb)
                    """,
                    (sid, client_ip, user_agent, json.dumps(meta or {})),
                )
        return sid
    except Exception as e:
        logger.warning("chat_log: create_session failed: %s", e, exc_info=True)
        return None


def append_message(
    session_id: str,
    role: str,
    content: str,
    meta: Optional[Dict[str, Any]] = None,
) -> None:
    """Append one message to chat_messages (user / assistant / system)."""
    if role not in ("user", "assistant", "system"):
        role = "user"
    try:
        with get_pool().connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO chat_messages (session_id, role, content, meta)
                    VALUES (%s::uuid, %s, %s, %s::jsonb)
                    """,
                    (session_id, role, content, json.dumps(meta or {})),
                )
    except Exception as e:
        logger.warning("chat_log: append_message failed: %s", e, exc_info=True)


def end_session(session_id: Optional[str]) -> None:
    """Set ended_at on chat_sessions."""
    if not session_id:
        return
    try:
        with get_pool().connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE chat_sessions
                    SET ended_at = now()
                    WHERE id = %s::uuid AND ended_at IS NULL
                    """,
                    (session_id,),
                )
    except Exception as e:
        logger.warning("chat_log: end_session failed: %s", e, exc_info=True)
