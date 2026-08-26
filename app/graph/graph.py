from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.graph.supervisor import supervisor_node
from app.graph.billing_agent import billing_node
from app.graph.technical_agent import technical_node
from app.graph.escalation_agent import escalation_node
from app.graph.refund_agent import refund_node
from app.graph.knowledge_agent import knowledge_node
from app.graph.checkpointer import checkpointer
from langgraph.types import Command


graph = StateGraph(AgentState)

graph.add_node("supervisor", supervisor_node)
graph.add_node("billing", billing_node)
graph.add_node("technical", technical_node)
graph.add_node("refund", refund_node)
graph.add_node("knowledge", knowledge_node)
graph.add_node("escalation", escalation_node)

graph.add_edge(START, "supervisor")


#router function
def route_from_supervisor(state: AgentState) -> str:
    """This function routes the graph to specific node based on intent of user."""

    next_node = state['next']

    if next_node == "billing":
        return "billing_edge"
    elif next_node == "technical":
        return "technical_edge"
    elif next_node == "refund":
        return "refund_edge"
    elif next_node == "knowledge":
        return "knowledge_edge"
    elif next_node == "escalation":
        return "escalation_edge"
    elif next_node == "end":
        return "end_edge"

graph.add_conditional_edges(
    "supervisor",
    route_from_supervisor,
    {
        #edge : node
        "billing_edge" : "billing",
        "technical_edge" : "technical",
        "refund_edge" : "refund",
        "knowledge_edge" : "knowledge",
        "escalation_edge" : "escalation",
        "end_edge" : END
    }
)

graph.add_edge("billing", END)
graph.add_edge("technical", END)
graph.add_edge("refund", END)
graph.add_edge("knowledge", END)
graph.add_edge("escalation", END)


app = graph.compile(checkpointer=checkpointer)

config = {"configurable" : {"thread_id" : "kb-thread-1"}}

result = app.invoke({
    "messages" : [("user", "Do you offer a student discount?")],
    "iterations" : 0,
    "next" : None,
    "intent" : None,
    "confidence" : None
}, config=config)

# result2 = app.invoke(Command(resume={"approved" : True}), config=config)
