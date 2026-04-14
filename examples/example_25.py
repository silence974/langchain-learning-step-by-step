from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END


class PizzaState(TypedDict):
    order_id: str
    size: str
    toppings: list
    current_step: str
    

def prepare_dough(state: PizzaState) -> PizzaState:
    print(f"准备 {state["size"]} 尺寸的面团")
    state["current_step"] = "dough_ready"
    return state


builder = StateGraph(PizzaState)
builder.add_node("prepare_dough", prepare_dough)

builder.add_edge(START, "prepare_dough")
builder.add_edge("prepare_dough", END)



from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers.
    """
    return a * b


tools = [multiply]
model_with_tools = model.bind_tools(tools)


response = model_with_tools.invoke("Add 3 and 4")
print(response.tool_calls)
