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
import re
from typing import Any, Dict, List, Optional

import httpx

from app.db import get_pool

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org"

# https://… до пробела/скобки/кавычек (типичные хвосты markdown)
_URL_RE = re.compile(r"https?://[^\s\)\]\"\'<>]+", re.IGNORECASE)


def _extract_calendar_urls_from_texts(texts: List[str]) -> List[str]:
    """Уникальные ссылки на Google Calendar из текстов ответов ассистента."""
    found: List[str] = []
    seen: set[str] = set()
    for raw in texts:
        if not raw:
            continue
        for m in _URL_RE.finditer(raw):
            u = m.group(0).rstrip(".,;)]}\"'")
            low = u.lower()
            if "calendar.app.google" in low or "calendar.google.com" in low:
                if u not in seen:
                    seen.add(u)
                    found.append(u)
    return found


def _telegram_href(url: str) -> str:
    """& в href для Telegram HTML."""
    return url.replace("&", "&amp;")


def diagnostics() -> Dict[str, Any]:
    """
    Безопасная сводка для /api/health: не раскрывает токен и chat_id.
    """
    token_set = bool(os.getenv("TELEGRAM_BOT_TOKEN", "").strip())
    chat_raw = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    chat_set = bool(chat_raw)
    raw_flag = os.getenv("TELEGRAM_NOTIFY_ENABLED", "true").strip().lower()
    flag_off = raw_flag in ("0", "false", "no", "off")
    return {
        "notify_env_flag_off": flag_off,
        "bot_token_configured": token_set,
        "chat_id_configured": chat_set,
        "would_attempt_send": (not flag_off) and token_set and chat_set,
        "chat_id_parseable_as_int": bool(
            chat_raw.lstrip("-").isdigit() if chat_raw else False
        ),
    }


def _enabled() -> bool:
    raw = os.getenv("TELEGRAM_NOTIFY_ENABLED", "true").strip().lower()
    if raw in ("0", "false", "no", "off"):
        return False
    return bool(os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"))


def _session_summary(session_id: str) -> Optional[Dict[str, Any]]:
    try:
        with get_pool().connection() as conn:
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
                cur.execute(
                    """
                    SELECT content
                    FROM chat_messages
                    WHERE session_id = %s::uuid AND role = 'assistant'
                    ORDER BY created_at ASC
                    """,
                    (session_id,),
                )
                assistant_texts = [r["content"] for r in cur.fetchall() if r.get("content")]
                calendar_urls = _extract_calendar_urls_from_texts(assistant_texts)
                if calendar_urls:
                    calendar_hint = True
        return {
            "started_at": row.get("started_at"),
            "ended_at": row.get("ended_at"),
            "client_ip": row.get("client_ip"),
            "counts": counts,
            "calendar_hint": calendar_hint,
            "calendar_urls": calendar_urls,
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


def _send_text(text: str, chat_id, token: str) -> None:
    """Low-level: send an HTML message to Telegram. Best-effort, logs on failure."""
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
            body = r.json() if r.content else {}
            if r.status_code != 200 or (isinstance(body, dict) and body.get("ok") is False):
                logger.warning("telegram_notify: send failed HTTP %s: %s", r.status_code, str(body)[:300])
            else:
                logger.warning("telegram_notify: sent OK chat_id=%s", chat_id)
    except Exception as e:
        logger.warning("telegram_notify: request failed: %s", e, exc_info=True)


def notify_session_ended(session_id: str) -> None:
    """Best-effort: send one message to Telegram after a chat session closes."""
    if not session_id:
        return
    if not _enabled():
        # WARNING: в Cloud Run по умолчанию часто не видны логи уровня INFO
        logger.warning(
            "telegram_notify: SKIPPED — выключено (TELEGRAM_NOTIFY_ENABLED) "
            "или нет TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID в переменных окружения"
        )
        return

    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id_raw = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id_raw:
        logger.warning(
            "telegram_notify: SKIPPED — пустой токен или chat_id после trim"
        )
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
        calendar_urls = summary.get("calendar_urls") or []
        if calendar_urls:
            text += "\n\n<b>Ссылка на встречу (календарь):</b>\n"
            for i, u in enumerate(calendar_urls, 1):
                href = _telegram_href(u)
                text += f'{i}. <a href="{href}">{html.escape(u)}</a>\n'

    _send_text(text, chat_id, token)


def notify_url_shared(
    shared_url: str,
    session_id: Optional[str],
    client_ip: Optional[str],
    context: Optional[str] = None,
) -> None:
    """Best-effort: notify Valerii when a visitor shares a link in chat."""
    if not _enabled():
        return
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id_raw = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id_raw:
        return
    chat_id = _parse_chat_id(chat_id_raw)

    safe_url = html.escape(shared_url)
    href = _telegram_href(shared_url)
    ip_str = html.escape(str(client_ip or "—"))
    sid_str = html.escape(str(session_id or "—"))
    ctx_str = html.escape((context or "")[:300])

    text = (
        "🔗 <b>Новая ссылка от посетителя</b>\n\n"
        f'URL: <a href="{href}">{safe_url}</a>\n'
        f"IP: {ip_str}\n"
        f"session: <code>{sid_str}</code>"
    )
    if ctx_str:
        text += f"\n\nКонтекст:\n{ctx_str}"

    _send_text(text, chat_id, token)


def send_test_message() -> Dict[str, Any]:
    """Одно тестовое сообщение в Telegram (для диагностики)."""
    if not _enabled():
        return {"ok": False, "error": "telegram not configured or disabled"}
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id_raw = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    chat_id = _parse_chat_id(chat_id_raw)
    tg_url = f"{TELEGRAM_API}/bot{token}/sendMessage"
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.post(tg_url, json={
                "chat_id": chat_id,
                "text": "AI Avatar: тестовое сообщение (диагностика Cloud Run → Telegram).",
            })
            body = r.json() if r.content else {}
            if r.status_code == 200 and isinstance(body, dict) and body.get("ok"):
                return {"ok": True, "telegram": body}
            return {"ok": False, "http_status": r.status_code,
                    "telegram": body if isinstance(body, dict) else r.text[:500]}
    except Exception as e:
        return {"ok": False, "error": str(e)}
