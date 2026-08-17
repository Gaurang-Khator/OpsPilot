from pydantic import BaseModel

class CustomerOut(BaseModel):
    id: int
    name: str
    email: str

class ConversationOut(BaseModel):
    id: int
    customer_id: int
    status: str

class MessageOut(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str

class ToolError(BaseModel):
    error: str