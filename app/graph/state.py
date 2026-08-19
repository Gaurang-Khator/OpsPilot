from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages : Annotated[list, add_messages]
    iterations : int
    next : str
    intent : str
    confidence : float 