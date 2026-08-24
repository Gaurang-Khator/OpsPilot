from app.tools.refund_tools import create_refund
from app.tools.order_tools import check_refund_eligibility, get_order
from app.graph.state import AgentState
from app.tools.schemas import ToolError

from langgraph.types import interrupt
from langchain_core.messages import AIMessage


APPROVAL_THRESHOLD = 100.00

#harcoded for testing until real order_id extraction
TEST_ORDER_ID = 1

def refund_node(state: AgentState) -> dict:

    order_id = TEST_ORDER_ID

    eligibility = check_refund_eligibility(order_id)

    if not eligibility["eligible"]:
        return { "messages" : [AIMessage(content=eligibility["reason"])], "next" : "end" }

    order = get_order(order_id)

    if isinstance(order, ToolError):
        return { "messages" : [AIMessage(content=order.error)], "next" : "end" }


    if order.amount > APPROVAL_THRESHOLD:

        decision = interrupt(
            {
                "action" : "approve_refund",
                "order_id" : order_id,
                "amount" : order.amount,
                "message" : f"Refund of Rs.{order.amount} for order {order_id} requires Human Approval.",
            }
        )

        if not decision.get("approved"):
            return { "messages" : [AIMessage(content="The refund was not approved by our team.")], "next" : "end" }

    #approved - create refund now
    result = create_refund(order_id, order.amount)

    if isinstance(result, ToolError):
        return { "messages" : [AIMessage(content=f"Refund failed: {result.error}")], "next" : "end" }

    return {
        "messages" : [AIMessage(content=f"Your refund of amount {result.amount} has been processed. (Refund Id : {result.id})")],
        "next" : "end"
    }