from app.tools.log_tools import search_logs_tool
from app.core.llm import get_llm
from app.graph.state import AgentState

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage


@tool
def search_logs(keyword: str) -> str:
    """Search the system/application logs containing the given keyword (case-insensitive)."""

    logs = search_logs_tool(keyword)

    return str(logs)


TECHNICAL_SYSTEM_PROMPT = """You are the technical support agent. Diagnose issues using log search. Be evidence-based — cite what the logs show, and say so clearly if nothing relevant was found."""


def technical_node(state: AgentState) -> dict:

    llm = get_llm("worker").bind_tools([search_logs])

    messages = [ SystemMessage(content=TECHNICAL_SYSTEM_PROMPT) ] + state["messages"]

    response = llm.invoke(messages)
    messages.append(response)

    while response.tool_calls:
        for call in response.tool_calls:
            tool_fn = {"search_logs" : search_logs}[call["name"]]
            result = tool_fn.invoke(call["args"])

            messages.append(ToolMessage(content=result, tool_call_id=call["id"]))

        response = llm.invoke(messages)
        messages.append(response)

    return { "messages" : [AIMessage(content=response.content)], "next" : "end" }

