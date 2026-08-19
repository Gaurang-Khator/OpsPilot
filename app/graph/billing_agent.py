from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool

from app.graph.state import AgentState
from app.core.llm import get_llm
from app.tools.billing_tools import get_invoices_by_customer
from app.tools.customer_tools import get_customer_by_email


@tool
def customer_lookup(email: str) -> str:
    """Look up a customer's account by their email address."""

    return get_customer_by_email(email).model_dump_json()

@tool
def invoices_lookup(customer_id: int) -> str:
    """Returns all the invoices of a customer by their customer id."""

    invoices = get_invoices_by_customer(customer_id)

    return str( [i.model_dump() for i in invoices] )


BILLING_SYSTEM_PROMPT = """You are the billing support agent. Help the user with invoice, payment, and charge questions. Use tools to look up real data -- never invent invoice details. If you need the customer's ID, look it up by email first."""


tools = [customer_lookup, invoices_lookup]

def billing_node(state: AgentState) -> dict:

    llm = get_llm("worker").bind_tools(tools)

    messages = [ SystemMessage(content=BILLING_SYSTEM_PROMPT) ] + state["messages"]

    # first call -- model decides whether it needs a tool
    response = llm.invoke(messages)
    # print("TOOL_CALLS:", response.tool_calls)
    # print("INVALID_TOOL_CALLS:", response.invalid_tool_calls)
    messages.append(response)

    # agent loop: keep running tool calls until the model replies with plain text
    while response.tool_calls:
        for call in response.tool_calls:
            tool_fn = {"customer_lookup" : customer_lookup, "invoices_lookup" : invoices_lookup}[call["name"]]
            result = tool_fn.invoke(call["args"])

            messages.append(ToolMessage(content=result, tool_call_id=call["id"]))

        response = llm.invoke(messages)
        # print("TOOL_CALLS:", response.tool_calls)
        # print("INVALID_TOOL_CALLS:", response.invalid_tool_calls)
        messages.append(response)

    return { "messages" : [AIMessage(content=response.content)], "next" : "end" }
