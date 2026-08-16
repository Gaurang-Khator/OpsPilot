import logging

from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    logger.info(
        "chat_request_recieved",
        extra={"conversation_id" : payload.conversation_id, "message_length": len(payload.message)},
    )

    reply = f"(stub) recieved: {payload.message}"

    return ChatResponse(conversation_id=payload.conversation_id, reply=reply)