from typing import TypedDict, Any

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.memory import InMemorySaver

from .tiger_gateway_client import TigerGatewayClient
from .sql_tools import execute_select
from .safety import validate_sql
from .memory import MemoryManager


class AgentState(TypedDict):
    question: str
    sql: str
    rows: list[dict[str, Any]]
    answer: str
    error: str
    history: list[dict]


class SQLAgentGraph:

    def __init__(self, connection):

        self.connection = connection
        self.client = TigerGatewayClient()

        self.memory = InMemorySaver()

        workflow = StateGraph(AgentState)

        workflow.add_node("generate_sql", self.generate_sql)
        workflow.add_node("validate_sql", self.validate_sql_node)
        workflow.add_node("execute_sql", self.execute_sql)
        workflow.add_node("summarize", self.summarize)
        
        workflow.set_entry_point("generate_sql")
        workflow.add_edge("generate_sql", "validate_sql")
        workflow.add_edge("validate_sql", "execute_sql")
        workflow.add_edge("execute_sql", "summarize")
        workflow.add_edge("summarize", END)

        self.graph = workflow.compile(
            checkpointer=self.memory
        )

    def schema_hint(self):

        return """
stores(
    store_id,
    store_name,
    region,
    city,
    store_type
)

products(
    product_id,
    product_name,
    category,
    sub_category,
    base_price
)

customers(
    customer_id,
    customer_segment,
    signup_date,
    preferred_channel,
    city
)

sales_transactions(
    order_id,
    order_date,
    store_id,
    product_id,
    customer_id,
    sales_channel,
    units_sold,
    unit_price,
    discount_pct INT (stored as a percentage from 0 to 100; e.g., 20 means a 20% discount. Divide by 100 when calculating discounted prices or revenue),
    payment_status,
    delivery_status
)

returns(
    return_id,
    order_id,
    return_date,
    return_reason
)
"""

    #################################################################

    def generate_sql(self, state: AgentState):

        history = MemoryManager.format_history(
            state.get("history", [])
        )

        sql = self.client.generate_sql(
            question=state["question"],
            schema=self.schema_hint(),
            history=history,
        )

        return {
            "sql": sql
        }

    #################################################################

    def validate_sql_node(self, state: AgentState):

        try:

            sql = validate_sql(state["sql"])

            return {
                "sql": sql
            }

        except Exception as e:

            return {
                "error": str(e)
            }

    #################################################################

    def execute_sql(self, state: AgentState):

        if state.get("error"):

            return {}

        rows = execute_select(
            state["sql"],
            self.connection
        )

        return {
            "rows": rows
        }

    #################################################################

    def summarize(self, state: AgentState):

        if state.get("error"):

            return {
                "answer": state["error"]
            }

        answer = self.client.summarize(
            question=state["question"],
            sql=state["sql"],
            rows=state["rows"]
        )
        
        history = MemoryManager.add_interaction(
            {
                **state,
                "answer": answer
            }
        )

        return {
            "answer": answer,
            "history": history
        }

    #################################################################

    def invoke(self, question: str):

        thread = {
            "configurable": {
                "thread_id": "1"
            }
        }

        return self.graph.invoke(
            {
                "question": question,
                "sql": "",
                "rows": [],
                "answer": "",
                "error": "",
            },
            config=thread,
        )