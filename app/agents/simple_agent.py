from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

from app.core.llm import get_llm
from app.tools.customer_tools import get_customer_by_email


@tool
def customer_lookup(email: str) -> str:
    """Look up a customer's account by their email address."""

    result = get_customer_by_email(email)

    return result.model_dump_json() #converts the Pydantic model(CustomerOut) to a JSON string.


tools = [customer_lookup]

def run_simple_agent(user_message: str) -> str:
    llm = get_llm("worker").bind_tools(tools)

    messages = [
        SystemMessage(content="You are a customer support assistant. Use tools to look up real data."),
        HumanMessage(content=user_message)
    ]

    # first call -- model decides whether it needs a tool
    response = llm.invoke(messages)
    messages.append(response)

    # agent loop: keep running tool calls until the model replies with plain text
    while response.tool_calls:
        for call in response.tool_calls:
            if call['name'] == "customer_lookup":
                result = customer_lookup.invoke(call['args'])
            else:
                result = f"Unknown tool: {call['name']}"

            messages.append(ToolMessage(content=result, tool_call_id=call['id']))

        response = llm.invoke(messages)
        messages.append(response)

    return response.content
