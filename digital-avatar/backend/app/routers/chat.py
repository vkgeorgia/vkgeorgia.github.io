import asyncio
import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app import chat_log, telegram_notify
from app.deps import rag_service
from app.services.resume_service import generate_resume

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_MESSAGE_LENGTH = 8000   # raised to allow full vacancy texts
MAX_HISTORY_TURNS = 10      # keep last N user+assistant pairs in Gemini context
VACANCY_MIN_LENGTH = 400    # shorter messages are never vacancies

# Keywords that signal a job vacancy in either language (2+ hits = vacancy)
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


def _is_vacancy_text(text: str) -> bool:
    """Heuristic: long text with 2+ vacancy keywords."""
    if len(text) < VACANCY_MIN_LENGTH:
        return False
    tl = text.lower()
    return sum(1 for kw in _VACANCY_KW if kw in tl) >= 2


def _is_russian(text: str) -> bool:
    ru = sum(1 for c in text if "\u0400" <= c <= "\u04ff")
    return ru > len(text) * 0.1


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
                    response_text = await _handle_vacancy(data, session_id, websocket)
                else:
                    response_text = await rag_service.generate_response(data, history=history)
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


async def _handle_vacancy(
    vacancy_text: str,
    session_id: Optional[str],
    websocket: WebSocket,
) -> str:
    """Detect vacancy → generate tailored resume → return markdown."""
    ru = _is_russian(vacancy_text)

    # Send immediate acknowledgement so user knows something is happening
    wait_msg = (
        "Анализирую вакансию и подготавливаю резюме — это займёт около 30 секунд…"
        if ru else
        "Analysing the vacancy and generating your tailored resume — this takes about 30 seconds…"
    )
    await websocket.send_text(wait_msg)

    try:
        result = await generate_resume(
            vacancy_text=vacancy_text,
            chat_session_id=session_id,
            source="bot",
        )
        intro = "Резюме готово:\n\n" if ru else "Here is your tailored resume:\n\n"
        return intro + result["content_md"]

    except ValueError as e:
        logger.warning(f"Resume generation (chat) — no projects: {e}")
        return (
            f"Не удалось подобрать релевантные проекты для этой вакансии: {e}"
            if ru else
            f"Could not find relevant projects for this vacancy: {e}"
        )
    except Exception as e:
        logger.error(f"Resume generation (chat) failed: {e}", exc_info=True)
        # Graceful fallback to RAG
        return await rag_service.generate_response(vacancy_text)
