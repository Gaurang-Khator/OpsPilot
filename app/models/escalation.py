from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, ForeignKey, Text
from app.db.session import Base


class Escalation(Base):
    __tablename__ = "escalations"

    id : Mapped[int] = mapped_column(primary_key=True)
    conversation_id : Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True)
    reason : Mapped[str] = mapped_column(Text)
    status : Mapped[str] = mapped_column(String(50), default="pending") # pending / resolved
    created_at : Mapped[datetime] = mapped_column(DateTime, default=lambda : datetime.now(timezone.utc))

