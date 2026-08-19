from app.core.llm import get_llm
from app.graph.state import AgentState
from langchain_core.messages import SystemMessage

from pydantic import BaseModel, Field
from typing import Literal

MAX_ITERATIONS_ALLOWED = 5


class routingDecision(BaseModel):
    intent : Literal["billing", "technical", "refund", "knowledge", "escalation", "end"]
    confidence : float = Field(ge=0.0 , le=1.0)
    reason: str


SUPERVISOR_SYSTEM_PROMPT = """You are a routing supervisor for a customer support system. Classify the user's latest message into exactly one category:
- billing: payment, invoices, charges
- technical: bugs, errors, how something works
- refund: wants money back, order cancellation
- knowledge: general FAQ questions
- escalation: user explicitly wants a human, or is angry/frustrated
- end: the conversation is resolved, nothing more to do
 
Respond with your routing decision."""


def supervisor_node(state: AgentState) -> dict:

    if state['iterations'] >= MAX_ITERATIONS_ALLOWED:

        return { "next" : "escalation", "iterations" : state["iterations"]+1 }


    llm = get_llm("supervisor").with_structured_output(routingDecision)

    all_messages = [SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT)] + state["messages"] 

    decision = llm.invoke(all_messages)

    return {
        "next" : decision.intent , 
        "intent" : decision.intent,
        "confidence" : decision.confidence,
        "iterations" : state["iterations"] + 1
    }

