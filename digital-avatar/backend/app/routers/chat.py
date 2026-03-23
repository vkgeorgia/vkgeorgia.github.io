import asyncio
import logging
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

@router.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id: Optional[str] = None
    history: List[Dict[str, str]] = []

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

            history.append({"role": "user", "content": data})

            try:
                if _is_vacancy_text(data):
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

            # Trim to last MAX_HISTORY_TURNS pairs
            if len(history) > MAX_HISTORY_TURNS * 2:
                history = history[-(MAX_HISTORY_TURNS * 2):]

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
