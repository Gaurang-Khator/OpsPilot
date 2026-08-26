from langchain_core.messages import AIMessage, ToolMessage, SystemMessage
from langchain.tools import tool

from app.core.llm import get_llm
from app.tools.knowledge_tools import search_knowledge_base_tool
from app.graph.state import AgentState


@tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base (FAQs, refund policy, account help) for relevant info."""

    results = search_knowledge_base_tool(query)

    if not results:
        return "No relevant documents found."

    return str(results)


KNOWLEDGE_SYSTEM_PROMPT = """You are the knowledge base assistant. Answer ONLY using information retrieved from the knowledge base tool -- never invent facts or policies. 
Always cite the source filename for any claim you make. If the retrieved chunks don't contain a relevant answer, 
say so clearly and suggest the user contact support or rephrase their question -- do not guess."""

tools = [search_knowledge_base]


def knowledge_node(state: AgentState) -> dict:

    llm = get_llm("worker").bind_tools(tools)

    messages = [SystemMessage(content=KNOWLEDGE_SYSTEM_PROMPT)] + state['messages']

    response = llm.invoke(messages)

    messages.append(response)

    while response.tool_calls:
        for call in response.tool_calls:
            tool_fn = {"search_knowledge_base" : search_knowledge_base}[call["name"]]

            result = tool_fn.invoke(call["args"])

            messages.append(ToolMessage(content=result, tool_call_id=call["id"]))


        response = llm.invoke(messages)

        messages.append(response)

    return { "messages" : [AIMessage(content=response.content)], "next" : "end" }