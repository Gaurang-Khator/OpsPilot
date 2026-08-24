import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from app.graph.supervisor import supervisor_node
from langchain_core.messages import HumanMessage

from app.tools.billing_tools import get_invoices_by_customer

from app.graph.graph import result, result2

if __name__ == "__main__":

    # result = supervisor_node({
    #     "messages": [HumanMessage(content="Where is my invoice of order 45")],
    #     "iterations": 0,
    # })
    # print(result)

    # print(result["messages"][-1].content)

    print(result)
    print(result2)

    # print(get_invoices_by_customer(12))
