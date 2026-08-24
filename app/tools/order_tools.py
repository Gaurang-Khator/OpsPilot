from app.db.session import SessionLocal
from app.tools.schemas import ToolError, OrderOut
from app.models.order import Order


def get_order(order_id: int) -> OrderOut | ToolError:
    """Fetch details of order by it's order id."""

    db = SessionLocal()

    try:
        order = db.query(Order).filter(Order.id == order_id).first()

        if order is None:
            return ToolError(error=f"No order found with order id: {order_id}")

        return OrderOut(id=order.id, customer_id=order.customer_id, amount=order.amount, status=order.status)

    finally:
        db.close()


def check_refund_eligibility(order_id: int) -> dict:
    """Checks for eligibility of refund for a given order id and returns eligible or not (True / False) and it's reason."""

    order_details = get_order(order_id)

    if isinstance(order_details, ToolError):
        return {"eligible": False, "reason": order_details.error}

    if order_details.status != "completed":
        return {"eligible": False, "reason": f"Order status is {order_details.status}, not eligible for refund."}

    return {"eligible": True, "reason": "Order is eligible for refund."}