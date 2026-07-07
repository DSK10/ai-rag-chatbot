from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.services.ollama_client import get_chat_reply, OllamaUnavailableError
from app.services.db import save_message
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    message_id = req.message_id or uuid.uuid4()
    try:
        reply = await get_chat_reply(req.text)
    except OllamaUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))

    try:
        await save_message(message_id, req.text, reply)
    except Exception:
        logger.exception("Failed to persist message %s", message_id)

    return ChatResponse(reply=reply, message_id=message_id)
