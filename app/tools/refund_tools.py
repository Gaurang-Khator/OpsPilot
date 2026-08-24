from app.db.session import SessionLocal
from app.models.refund import Refund
from app.models.order import Order
from app.tools.schemas import RefundOut, ToolError
from app.tools.order_tools import get_order


def create_refund(order_id: int, amount: float) -> RefundOut | ToolError:
    """Creates a refund for an order and marks the order as refunded."""

    order_details = get_order(order_id)

    if isinstance(order_details, ToolError):
        return order_details

    if order_details.status != "completed":
        return ToolError(error=f"Order {order_id} is not eligible for refund.(status = {order_details.status})")

    db = SessionLocal()

    try:

        refund = Refund(order_id=order_id, amount=amount, status="completed")

        db.add(refund)
        #update the order status in the SAME transaction as the refund insert -- both succeed together or both roll back, 
        #avoiding a state where a refund exists but the order still shows "completed"

        order = db.query(Order).filter(Order.id == order_id).first()
        order.status = "refunded"

        db.commit()

        db.refresh(refund)

        return RefundOut(id=refund.id, order_id=refund.order_id, amount=float(refund.amount), status=refund.status)

    finally:
        db.close()