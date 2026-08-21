from app.db.session import SessionLocal
from app.tools.schemas import EscalationOut, ToolError
from app.models.escalation import Escalation
from app.models.conversation import Conversation


def create_escalation(conversation_id: int, reason: str) -> EscalationOut | ToolError:
    """Creates a new escalation thread for a customer."""

    if not reason.strip():
        return ToolError(error="Escalation reason cannot be empty.")

    db = SessionLocal()

    try:
        escalation = Escalation(conversation_id=conversation_id, reason=reason, status="pending")
        db.add(escalation)
        db.commit()
        db.refresh(escalation)

        return EscalationOut(id=escalation.id, conversation_id=escalation.conversation_id, reason=escalation.reason, status=escalation.status)

    finally:
        db.close()