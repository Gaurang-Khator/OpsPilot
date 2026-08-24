from datetime import datetime, timezone
from sqlalchemy import String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import mapped_column, Mapped
from app.db.session import Base


class Refund(Base):
    __tablename__ = "refunds"

    id : Mapped[int] = mapped_column(primary_key=True)
    order_id : Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(50), default="pending_approval") # pending_approval / approved / rejected / completed
    created_at : Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))