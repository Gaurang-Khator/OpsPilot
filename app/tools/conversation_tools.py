from app.db.session import SessionLocal

from app.models.conversation import Conversation
from app.models.message import Message
from app.tools.schemas import ConversationOut, MessageOut, ToolError


def create_conversation(customer_id: int) -> ConversationOut | ToolError:
    """Creates a new conversation thread for a customer."""

    db = SessionLocal()

    try:
        conversation = Conversation(customer_id=customer_id, status="open")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return ConversationOut(id=conversation.id, customer_id=conversation.customer_id, status=conversation.status)

    finally:
        db.close()


def save_message(conversation_id: int, role: str, content: str) -> MessageOut | ToolError:
    """Save a message(user or assistant) into a conversation."""

    if role not in ("user", "assistant"):
        return ToolError(error=f"Invalid role: {role}")

    db = SessionLocal()

    try:
        message = Message(conversation_id=conversation_id, role=role, content=content)
        db.add(message)
        db.commit()
        db.refresh(message)

        return MessageOut(id=message.id, conversation_id=message.conversation_id, role=message.role, content=message.content)

    finally:
        db.close()


def get_conversation_history(conversation_id: int) -> list[MessageOut]:
    """Fetch all messages in a conversation, oldest first."""

    db = SessionLocal()

    try:
        messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()

        return [ MessageOut(id=m.id, conversation_id=m.conversation_id, role=m.role, content=m.content) for m in messages ]

    finally:
        db.close()