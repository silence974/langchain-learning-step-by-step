# subgraph 01

from typing_extensions import TypedDict
from langgraph.graph.state import StateGraph, START


class SubgraphState(TypedDict):
    bar: str
    

def subgraph_node_1(state: SubgraphState) -> SubgraphState:
    return {"bar": "hi!" + state["bar"]}


subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node("subgraph_node_1", subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()



class State(TypedDict):
    foo: str


def call_subgraph(state: State) -> State:
    subgraph_output = subgraph.invoke({"bar": state["foo"]})
    return {"foo": subgraph_output["bar"]}

builder = StateGraph(State)
builder.add_node("node_1", call_subgraph)
builder.add_edge(START, "node_1")
graph = builder.compile()