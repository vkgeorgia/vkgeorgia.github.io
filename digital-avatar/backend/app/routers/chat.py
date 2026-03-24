import asyncio
import ipaddress
import logging
import re
from typing import Dict, List, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app import chat_log, telegram_notify
from app.deps import rag_service
from app.services.resume_service import generate_resume, _call_llm

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_MESSAGE_LENGTH = 8000   # raised to allow full vacancy texts
MAX_HISTORY_TURNS = 10      # keep last N user+assistant pairs in Gemini context
VACANCY_MIN_LENGTH = 400    # shorter messages are never standalone vacancies
MAX_URLS_PER_SESSION = 3    # rate-limit: max shared links per session
URL_MAX_LENGTH = 500

_RAW_URL_RE = re.compile(r'https?://[^\s<>"\']{4,}', re.IGNORECASE)

# Private/loopback hostnames and IP prefixes to block
_BLOCKED_HOSTS = re.compile(
    r'^(localhost|.*\.local|.*\.internal|.*\.localdomain)$', re.IGNORECASE
)
_PRIVATE_IP_NETS = [
    ipaddress.ip_network(n) for n in (
        "127.0.0.0/8", "10.0.0.0/8", "172.16.0.0/12",
        "192.168.0.0/16", "169.254.0.0/16", "::1/128", "fc00::/7",
    )
]


def _validate_url(raw: str) -> Optional[str]:
    """Return cleaned URL if safe, None otherwise."""
    url = raw.rstrip(".,;)>\"'")
    if len(url) > URL_MAX_LENGTH:
        return None
    if not re.match(r'^https?://', url, re.IGNORECASE):
        return None
    # Extract hostname
    m = re.match(r'^https?://([^/:?#\s]+)', url, re.IGNORECASE)
    if not m:
        return None
    host = m.group(1).lower()
    if _BLOCKED_HOSTS.match(host):
        return None
    try:
        addr = ipaddress.ip_address(host)
        if any(addr in net for net in _PRIVATE_IP_NETS):
            return None
    except ValueError:
        pass  # not an IP literal — hostname is fine
    return url


def _extract_urls(text: str) -> List[str]:
    """Return list of valid URLs found in text."""
    found = []
    for m in _RAW_URL_RE.finditer(text):
        url = _validate_url(m.group(0))
        if url and url not in found:
            found.append(url)
    return found

# Keywords that signal a job vacancy (2+ hits = vacancy text)
_VACANCY_KW = [
    # English
    "responsibilities", "requirements", "qualifications",
    "we are looking", "job description", "about the role",
    "what you will do", "what you'll do", "must have",
    "nice to have", "years of experience", "bachelor",
    "we offer", "apply now",
    # Russian
    "обязанности", "требования", "квалификация",
    "мы ищем", "описание вакансии", "будет плюсом",
    "опыт работы", "что нужно", "желательно",
    "обязательно", "условия работы", "мы предлагаем",
]

# Keywords that signal resume-generation intent in a short message
_RESUME_INTENT_KW = [
    "резюме", "составь", "подготовь резюме", "напиши резюме",
    "сделай резюме", "resume", "write a resume", "prepare a resume",
    "generate resume", "create resume", "make a resume",
    "write me a cv", "write cv", "create cv",
]


def _is_vacancy_text(text: str) -> bool:
    """Long text with 2+ vacancy keywords → treat as pasted vacancy."""
    if len(text) < VACANCY_MIN_LENGTH:
        return False
    tl = text.lower()
    return sum(1 for kw in _VACANCY_KW if kw in tl) >= 2


def _has_resume_intent(text: str) -> bool:
    """Short message asking to write a resume."""
    tl = text.lower()
    return any(kw in tl for kw in _RESUME_INTENT_KW)


def _is_russian(text: str) -> bool:
    ru = sum(1 for c in text if "\u0400" <= c <= "\u04ff")
    return ru > len(text) * 0.1


# ---------------------------------------------------------------------------
# Vacancy extraction from conversation history
# ---------------------------------------------------------------------------

async def _extract_vacancy_from_history(
    history: List[Dict[str, str]],
    current_msg: str,
) -> Optional[str]:
    """Ask LLM to synthesise a vacancy description from conversation history.

    Returns a synthesised vacancy text (100+ chars) or None if there is
    not enough information in the conversation to generate a resume.
    """
    # Need at least a few prior turns to have context
    prior = [m for m in history[:-1] if m["role"] in ("user", "assistant")]
    if len(prior) < 2:
        return None

    conversation = "\n".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in prior[-20:]  # last 20 turns is plenty
    )

    system_prompt = (
        "You are a data extractor. Analyse a conversation and extract any job vacancy "
        "or position description mentioned by the user. "
        "Return ONLY the synthesised vacancy description as plain text. "
        "If there is not enough information to describe a specific role, return exactly: NO_VACANCY"
    )

    user_prompt = f"""Conversation so far:
{conversation}

Current user message: {current_msg}

Extract any job/position description from the conversation above.
If the user described a role they need to fill (industry, skills, responsibilities, requirements),
synthesise it into a vacancy description.
If there is not enough context, return exactly: NO_VACANCY"""

    try:
        result = await _call_llm(system_prompt, user_prompt)
        result = result.strip()
        if result == "NO_VACANCY" or len(result) < 80:
            return None
        return result
    except Exception as e:
        logger.warning(f"Vacancy extraction from history failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

async def _handle_vacancy(
    vacancy_text: str,
    session_id: Optional[str],
    websocket: WebSocket,
) -> str:
    """User pasted a full vacancy → generate resume immediately."""
    ru = _is_russian(vacancy_text)
    await websocket.send_text(
        "Анализирую вакансию и подготавливаю резюме — это займёт около 30 секунд…"
        if ru else
        "Analysing the vacancy and generating your tailored resume — about 30 seconds…"
    )
    try:
        result = await generate_resume(
            vacancy_text=vacancy_text,
            chat_session_id=session_id,
            source="bot",
        )
        intro = "Резюме готово:\n\n" if ru else "Here is your tailored resume:\n\n"
        return intro + result["content_md"]
    except ValueError as e:
        logger.warning(f"Resume generation (pasted vacancy): {e}")
        return (
            f"Не удалось подобрать релевантные проекты для этой вакансии: {e}"
            if ru else
            f"Could not find relevant projects for this vacancy: {e}"
        )
    except Exception as e:
        logger.error(f"Resume generation (pasted vacancy) failed: {e}", exc_info=True)
        return await rag_service.generate_response(vacancy_text)


async def _handle_resume_intent(
    data: str,
    history: List[Dict[str, str]],
    session_id: Optional[str],
    websocket: WebSocket,
) -> str:
    """User asked for a resume — try to extract vacancy from conversation history."""
    ru = _is_russian(data)

    vacancy = await _extract_vacancy_from_history(history, data)

    if not vacancy:
        # Not enough context in history — ask for vacancy text
        return (
            "Пришлите текст вакансии (описание позиции, требования, обязанности), "
            "и я подготовлю резюме, адаптированное под неё."
            if ru else
            "Please share the job vacancy description (role, requirements, responsibilities) "
            "and I will prepare a tailored resume for it."
        )

    # Enough context — generate resume from synthesised vacancy
    await websocket.send_text(
        "Нашёл описание позиции в нашем разговоре — готовлю резюме, ~30 секунд…"
        if ru else
        "Found position details in our conversation — generating resume, ~30 seconds…"
    )
    try:
        result = await generate_resume(
            vacancy_text=vacancy,
            chat_session_id=session_id,
            source="bot",
        )
        intro = (
            "Резюме на основе нашего разговора:\n\n"
            if ru else
            "Resume based on our conversation:\n\n"
        )
        return intro + result["content_md"]
    except ValueError as e:
        logger.warning(f"Resume generation (history intent): {e}")
        return (
            "Пришлите полный текст вакансии — в нашем разговоре недостаточно деталей "
            "чтобы подобрать релевантные проекты."
            if ru else
            "Please share the full vacancy text — the conversation doesn't have enough "
            "detail to match relevant projects."
        )
    except Exception as e:
        logger.error(f"Resume generation (history intent) failed: {e}", exc_info=True)
        return await rag_service.generate_response(data, history=history)


# ---------------------------------------------------------------------------
# WebSocket endpoint
# ---------------------------------------------------------------------------

async def _handle_url_share(
    urls: List[str],
    data: str,
    session_id: Optional[str],
    client_ip: Optional[str],
    url_count: int,
) -> str:
    """Forward shared URLs to Valerii via Telegram and return bot reply."""
    ru = _is_russian(data)

    if url_count >= MAX_URLS_PER_SESSION:
        return (
            "Вы уже поделились несколькими ссылками в этом разговоре — я передал их Валерию."
            if ru else
            "You've already shared several links this session — Valerii has been notified."
        )

    for url in urls:
        await asyncio.to_thread(
            telegram_notify.notify_url_shared,
            url, session_id, client_ip, data,
        )

    if ru:
        return (
            "Спасибо — ссылка передана Валерию, он свяжется с вами. "
            "Если хотите, можем продолжить разговор или я подготовлю резюме под вашу позицию."
        )
    return (
        "Thanks — the link has been forwarded to Valerii, he'll be in touch. "
        "Feel free to keep chatting, or share a vacancy and I'll prepare a tailored resume."
    )


@router.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id: Optional[str] = None
    history: List[Dict[str, str]] = []
    url_count: int = 0

    try:
        client_ip = websocket.client.host if websocket.client else None
        user_agent = websocket.headers.get("user-agent")
        session_id = await asyncio.to_thread(
            chat_log.create_session, client_ip, user_agent, None
        )

        while True:
            data = await websocket.receive_text()

            if len(data) > MAX_MESSAGE_LENGTH:
                await websocket.send_text(
                    f"Your message is too long. Please keep it under {MAX_MESSAGE_LENGTH} characters."
                )
                continue

            logger.info(f"Received message (len={len(data)})")

            if session_id:
                await asyncio.to_thread(
                    chat_log.append_message, session_id, "user", data, None
                )

            if len(history) >= MAX_HISTORY_TURNS * 2:
                history = history[-(MAX_HISTORY_TURNS * 2 - 2):]
            history.append({"role": "user", "content": data})

            try:
                urls = _extract_urls(data)
                if urls and not _is_vacancy_text(data):
                    # Pattern 0: user shared a link — forward to Valerii
                    response_text = await _handle_url_share(
                        urls, data, session_id, client_ip, url_count
                    )
                    url_count += len(urls)
                elif _is_vacancy_text(data):
                    # Pattern 1: user pasted a full vacancy text
                    response_text = await _handle_vacancy(data, session_id, websocket)
                elif _has_resume_intent(data):
                    # Pattern 2: user asked for resume — check conversation history
                    response_text = await _handle_resume_intent(
                        data, history, session_id, websocket
                    )
                else:
                    response_text = await rag_service.generate_response(
                        data, history=history
                    )
            except Exception as e:
                logger.error(f"Error generating response: {e}", exc_info=True)
                response_text = "Internal Error: Could not generate response."

            history.append({"role": "assistant", "content": response_text})


            if session_id:
                await asyncio.to_thread(
                    chat_log.append_message, session_id, "assistant", response_text, None
                )

            await websocket.send_text(response_text)

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Unexpected WebSocket error: {e}", exc_info=True)
        await websocket.close()
    finally:
        if session_id:
            await asyncio.to_thread(chat_log.end_session, session_id)
            await asyncio.to_thread(telegram_notify.notify_session_ended, session_id)
