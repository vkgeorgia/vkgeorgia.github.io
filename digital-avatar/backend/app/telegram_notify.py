"""
Send short Telegram notifications when a chat session ends.

Requires environment variables (Cloud Run / local .env):
  TELEGRAM_BOT_TOKEN  — from @BotFather
  TELEGRAM_CHAT_ID    — your user id or group id (string)

Optional:
  TELEGRAM_NOTIFY_ENABLED — set to "0" or "false" to disable without removing secrets.
"""
from __future__ import annotations

import html
import logging
import os
from typing import Any, Dict, Optional

import httpx

from app.db import get_db_connection

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org"


def _enabled() -> bool:
    raw = os.getenv("TELEGRAM_NOTIFY_ENABLED", "true").strip().lower()
    if raw in ("0", "false", "no", "off"):
        return False
    return bool(os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"))


def _session_summary(session_id: str) -> Optional[Dict[str, Any]]:
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT started_at, ended_at, client_ip
                    FROM chat_sessions
                    WHERE id = %s::uuid
                    """,
                    (session_id,),
                )
                row = cur.fetchone()
                if not row:
                    return None
                cur.execute(
                    """
                    SELECT role, COUNT(*)::int AS c
                    FROM chat_messages
                    WHERE session_id = %s::uuid
                    GROUP BY role
                    """,
                    (session_id,),
                )
                counts = {r["role"]: r["c"] for r in cur.fetchall()}
                cur.execute(
                    """
                    SELECT EXISTS (
                      SELECT 1 FROM chat_messages
                      WHERE session_id = %s::uuid
                        AND role = 'assistant'
                        AND (
                          content ILIKE %s
                          OR content ILIKE %s
                        )
                    ) AS cal
                    """,
                    (
                        session_id,
                        "%calendar.app.google%",
                        "%calendar.google%",
                    ),
                )
                cal_row = cur.fetchone()
                calendar_hint = bool(cal_row and cal_row.get("cal"))
        finally:
            conn.close()
        return {
            "started_at": row.get("started_at"),
            "ended_at": row.get("ended_at"),
            "client_ip": row.get("client_ip"),
            "counts": counts,
            "calendar_hint": calendar_hint,
        }
    except Exception as e:
        logger.warning("telegram_notify: session summary failed: %s", e, exc_info=True)
        return None


def _parse_chat_id(raw: str):
    """Telegram принимает chat_id как int (в т.ч. отрицательный для групп) или строку."""
    s = raw.strip()
    if s.lstrip("-").isdigit():
        return int(s)
    return s


def notify_session_ended(session_id: str) -> None:
    """Best-effort: send one message to Telegram after a chat session closes."""
    if not session_id:
        return
    if not _enabled():
        logger.info(
            "telegram_notify: skipped (TELEGRAM_NOTIFY_ENABLED off or missing "
            "TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID in env)"
        )
        return

    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id_raw = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id_raw:
        logger.info("telegram_notify: skipped (empty token or chat_id after strip)")
        return
    chat_id = _parse_chat_id(chat_id_raw)

    summary = _session_summary(session_id)
    if not summary:
        text = (
            f"AI Avatar: сессия чата завершена\n"
            f"session_id: <code>{html.escape(session_id)}</code>\n"
            f"(не удалось загрузить сводку из БД)"
        )
    else:
        counts = summary["counts"]
        n_user = counts.get("user", 0)
        n_asst = counts.get("assistant", 0)
        cal = "да" if summary.get("calendar_hint") else "нет"
        ip = summary.get("client_ip") or "—"
        started = summary.get("started_at")
        ended = summary.get("ended_at")
        text = (
            "🤖 <b>AI Avatar</b>: сессия чата завершена\n\n"
            f"session_id: <code>{html.escape(session_id)}</code>\n"
            f"сообщений: user={n_user}, assistant={n_asst}\n"
            f"упоминание календаря в ответах: {cal}\n"
            f"IP: {html.escape(str(ip))}\n"
            f"начало: {html.escape(str(started))}\n"
            f"конец: {html.escape(str(ended))}"
        )

    url = f"{TELEGRAM_API}/bot{token}/sendMessage"
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
            )
            try:
                body = r.json()
            except Exception:
                body = None
            if r.status_code != 200:
                logger.warning(
                    "telegram_notify: sendMessage HTTP %s %s",
                    r.status_code,
                    r.text[:800],
                )
            elif isinstance(body, dict) and body.get("ok") is False:
                logger.warning(
                    "telegram_notify: Telegram API ok=false: %s",
                    body.get("description", body),
                )
            else:
                logger.info(
                    "telegram_notify: sent session summary for %s (chat_id=%s)",
                    session_id,
                    chat_id,
                )
    except Exception as e:
        logger.warning("telegram_notify: request failed: %s", e, exc_info=True)
