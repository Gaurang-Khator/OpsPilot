from langchain_core.messages import AIMessage

from app.graph.state import AgentState
from app.tools.escalation_tools import create_escalation


def escalation_node(state: AgentState) -> dict:

    # reason comes from the supervisor's own classification -- no LLM call needed here,
    reason = state['intent'] or "User requested escalation or repeated attempts failed."

    # conversation_id is a client string; DB FK expects an int. Placeholder until persistence wiring.
    result = create_escalation(conversation_id=1, reason=reason)

    if hasattr(result, "error"):
        reply = "I wasn't able to log your escalation right now, but a human will still review this conversation."

    else:
        reply = (
            "I've escalated this to our support team -- a human will follow up with you shortly."
            f"(Escalation ID: {result.id})"
        )

    return { "messages" : [AIMessage(content=reply)], "next" : "end" }
