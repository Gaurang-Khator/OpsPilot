from langchain_core.messages import AIMessage
from app.graph.state import AgentState

def create_stub_worker(name: str):
    def node(state: AgentState) -> dict:
        return {"messages" : [AIMessage(content=f"[{name} worker stub] handled the request.")] , "next" : "end"}
    return node

billing_node = create_stub_worker("billing")
technical_node = create_stub_worker("technical")
refund_node = create_stub_worker("refund")
knowledge_node = create_stub_worker("knowledge")
escalation_node = create_stub_worker("escalation")