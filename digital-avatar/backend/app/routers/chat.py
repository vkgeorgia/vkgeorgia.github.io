import asyncio
import ipaddress
import logging
import re
from typing import Any, Dict, List, Optional

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

_CONTACT_KW = [
    # Explicit contact sharing
    "my email", "my phone", "contact me", "reach me", "you can reach",
    "send me", "write to me", "call me",
    # Russian
    "мой email", "мой телефон", "мой e-mail", "напишите мне",
    "свяжитесь", "мой контакт", "позвоните мне",
]

_EMAIL_RE = re.compile(r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b')
_PHONE_RE = re.compile(r'(?:\+?\d[\d\s\-\(\)]{7,}\d)')

_PERSONAL_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com",
    "msn.com", "mail.ru", "yandex.ru", "yandex.com", "icloud.com",
    "proton.me", "protonmail.com", "inbox.ru", "bk.ru", "list.ru",
    "rambler.ru", "ukr.net", "googlemail.com",
}

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
    # Normalize via IDNA to detect homograph attacks (e.g. Cyrillic lookalikes)
    try:
        host = host.encode("idna").decode("ascii")
    except (UnicodeError, UnicodeDecodeError):
        return None  # invalid or non-encodable hostname
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


def _extract_contact_info(text: str):
    """Returns (email, phone) found in text, or (None, None)."""
    email = _EMAIL_RE.search(text)
    phone = _PHONE_RE.search(text)
    return (
        email.group(0) if email else None,
        phone.group(0).strip() if phone else None,
    )


def _has_contact_intent(text: str) -> bool:
    """True if message contains actual contact data or contact-sharing keywords."""
    tl = text.lower()
    has_kw = any(kw in tl for kw in _CONTACT_KW)
    email, phone = _extract_contact_info(text)
    return bool(email or phone or has_kw)


async def _extract_name_from_history(history, current_msg: str) -> str:
    """Ask LLM to find the user's name from the conversation history."""
    if not history:
        return "Unknown"
    conversation = "\n".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in history[-10:]
    )
    system = (
        "You are a data extractor. Find the person's name from the conversation. "
        "Return ONLY the name as plain text, or 'Unknown' if not found."
    )
    prompt = (
        f"Conversation:\n{conversation}\n\n"
        f"Current message: {current_msg}\n\nWhat is the user's name?"
    )
    try:
        name = await _call_llm(system, prompt)
        return name.strip()[:100] or "Unknown"
    except Exception:
        return "Unknown"


def _is_work_email(email: str) -> bool:
    return email.split("@")[-1].lower() not in _PERSONAL_DOMAINS


def _ask_for_contact(ru: bool) -> str:
    if ru:
        return (
            "Прежде чем я подготовлю резюме — скажите, пожалуйста, ваше имя, "
            "рабочий email и компанию? Валерий сможет связаться с вами напрямую."
        )
    return (
        "Before I prepare the resume — could you share your name, "
        "work email, and company? That way Valerii can follow up with you directly."
    )


async def _parse_contact_reply(text: str) -> Dict[str, Any]:
    """Extract name, email, company from a free-text reply using LLM + regex fallback."""
    import json as _json
    system = (
        "You are a data extractor. Extract contact information from text. "
        "Return ONLY valid JSON with keys: name, email, company. "
        "Use null for missing fields. No explanation, just JSON."
    )
    try:
        raw = await _call_llm(system, f"Extract: {text}")
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        if m:
            data = _json.loads(m.group(0))
            return {
                "name": data.get("name"),
                "email": data.get("email"),
                "company": data.get("company"),
            }
    except Exception:
        pass
    email_m = _EMAIL_RE.search(text)
    return {"name": None, "email": email_m.group(0) if email_m else None, "company": None}


async def _detect_session_intent(history: List[Dict[str, str]]) -> str:
    """Classify visitor intent from conversation history using LLM."""
    if not history:
        return "general"
    conversation = "\n".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content'][:300]}"
        for m in history[-20:]
    )
    system = (
        "You are an intent classifier. Analyse the conversation and classify the visitor's primary intent.\n"
        "Return ONLY one of these labels:\n"
        "  employer  — recruiter or company looking to hire Valerii as employee or contractor\n"
        "  client    — business looking for consulting, project, or contract work from Valerii\n"
        "  partner   — potential business partner or collaborator\n"
        "  general   — general curiosity, no clear business intent\n"
        "Return exactly one word, nothing else."
    )
    try:
        result = await _call_llm(system, f"Conversation:\n{conversation}\n\nIntent:")
        label = result.strip().lower().split()[0]
        if label in ("employer", "client", "partner", "general"):
            return label
    except Exception as e:
        logger.warning(f"Intent detection failed: {e}")
    return "general"


async def _handle_contact_collection(
    data: str,
    session_state: Dict[str, Any],
    history: List[Dict[str, str]],
    session_id: Optional[str],
    client_ip: Optional[str],
    websocket: WebSocket,
) -> str:
    """Parse contact reply, validate, save lead, then execute the pending pattern."""
    ru = _is_russian(data)
    contact = await _parse_contact_reply(data)
    email = contact.get("email")
    name = contact.get("name") or "Unknown"

    if not email:
        return (
            "Не нашёл email в вашем сообщении. Пожалуйста, укажите рабочую почту."
            if ru else
            "I couldn't find an email address. Please share your work email."
        )

    if not _is_work_email(email):
        return (
            "Пожалуйста, укажите **рабочий** email (не Gmail/Yahoo/Яндекс и т.д.). "
            "Это нужно чтобы Валерий понял, с какой организацией вы связаны."
            if ru else
            "Please share a **work** email (not Gmail/Yahoo etc.). "
            "It helps Valerii know which organisation you're from."
        )

    session_state.update({
        "contact_verified": True,
        "awaiting_contact": False,
        "name": name,
        "email": email,
        "company": contact.get("company"),
    })

    try:
        await _handle_lead_capture(data, history, session_id, client_ip)
    except Exception as e:
        logger.error(f"Lead save after contact collection failed: {e}")

    pending = session_state.get("pending_pattern")
    pending_data = session_state.get("pending_data", data)

    if pending == "vacancy":
        return await _handle_vacancy(pending_data, session_id, websocket)
    elif pending == "resume_intent":
        return await _handle_resume_intent(pending_data, history, session_id, websocket)
    return (
        "Спасибо! Данные сохранены. Чем могу помочь?"
        if ru else
        "Thank you! Details saved. How can I help you?"
    )


async def _handle_lead_capture(
    data: str,
    history,
    session_id,
    client_ip: str,
) -> str:
    """Pattern 3: user shared contact info → save as lead in DB."""
    from app import db

    ru = _is_russian(data)
    email, phone = _extract_contact_info(data)
    name = await _extract_name_from_history(history, data)

    def _save_lead():
        with db.get_pool().connection() as conn:
            cur = conn.cursor()
            if email:
                cur.execute("SELECT id FROM contacts WHERE email = %s", (email,))
                existing = cur.fetchone()
                if existing:
                    cur.execute(
                        """
                        UPDATE contacts SET
                            chat_session_id = COALESCE(chat_session_id, %s::uuid),
                            status = CASE WHEN status = 'contact' THEN 'lead' ELSE status END,
                            updated_at = NOW()
                        WHERE id = %s
                        """,
                        (session_id, existing["id"]),
                    )
                    conn.commit()
                    return "updated"
            cur.execute(
                """
                INSERT INTO contacts
                  (full_name, email, phone, source, status, chat_session_id,
                   lead_score, notes)
                VALUES (%s, %s, %s, 'chatbot', 'lead', %s::uuid, 20, %s)
                ON CONFLICT DO NOTHING
                """,
                (name, email, phone, session_id, f"First contact via chatbot. Message: {data[:300]}"),
            )
            conn.commit()
            return "created"

    try:
        action = await asyncio.to_thread(_save_lead)
        logger.info(f"Lead {action}: email={email}, phone={phone}, session={session_id}")
    except Exception as e:
        logger.error(f"Lead capture failed: {e}", exc_info=True)

    if ru:
        return (
            "Спасибо! Я сохранил ваши контактные данные и передал их Валерию. "
            "Он свяжется с вами в ближайшее время. Если хотите — могу также "
            "подготовить резюме под вашу вакансию или ответить на другие вопросы."
        )
    return (
        "Thank you! I've saved your contact details and notified Valerii. "
        "He'll be in touch shortly. Feel free to ask more questions or share "
        "a vacancy and I'll prepare a tailored resume."
    )


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
    session_state: Dict[str, Any] = {
        "contact_verified": False,
        "awaiting_contact": False,
        "pending_pattern": None,
        "pending_data": None,
    }

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
                if session_state["awaiting_contact"]:
                    # Collecting contact info before resume generation
                    response_text = await _handle_contact_collection(
                        data, session_state, history, session_id, client_ip, websocket
                    )
                elif urls and not _is_vacancy_text(data):
                    # Pattern 0: user shared a link — forward to Valerii
                    response_text = await _handle_url_share(
                        urls, data, session_id, client_ip, url_count
                    )
                    url_count += len(urls)
                elif _is_vacancy_text(data):
                    # Pattern 1: vacancy text — require contact first
                    if not session_state["contact_verified"]:
                        session_state["awaiting_contact"] = True
                        session_state["pending_pattern"] = "vacancy"
                        session_state["pending_data"] = data
                        response_text = _ask_for_contact(_is_russian(data))
                    else:
                        response_text = await _handle_vacancy(data, session_id, websocket)
                elif _has_resume_intent(data):
                    # Pattern 2: resume intent — require contact first
                    if not session_state["contact_verified"]:
                        session_state["awaiting_contact"] = True
                        session_state["pending_pattern"] = "resume_intent"
                        session_state["pending_data"] = data
                        response_text = _ask_for_contact(_is_russian(data))
                    else:
                        response_text = await _handle_resume_intent(
                            data, history, session_id, websocket
                        )
                elif _has_contact_intent(data):
                    # Pattern 3: user shared contact info spontaneously → save as lead
                    response_text = await _handle_lead_capture(
                        data, history, session_id, client_ip
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
            intent = await _detect_session_intent(history) if history else "general"
            await asyncio.to_thread(chat_log.end_session, session_id)
            await asyncio.to_thread(telegram_notify.notify_session_ended, session_id, intent)
