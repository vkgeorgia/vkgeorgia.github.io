import asyncio
import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app import chat_log, telegram_notify
from app.deps import rag_service

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_MESSAGE_LENGTH = 2000
MAX_HISTORY_TURNS = 10  # keep last N user+assistant pairs in Gemini context


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
