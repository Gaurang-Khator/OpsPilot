from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    conversation_id: str = Field(..., description="Client-generated or existing thread id")
    message: str = Field(..., min_length=1, max_length=4000)

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    status: str = "ok"