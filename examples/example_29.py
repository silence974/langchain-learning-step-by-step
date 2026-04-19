from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
import uuid


class State(dict): pass


graph = StateGraph(State)
graph.add_node("slow_llm", lambda state: {"result": f"LLM-{uuid.uuid4()}"})
graph.add_edge(START, "slow_llm")

checkpointer = MemorySaver()
graph = graph.compile(checkpointer=checkpointer)

config = {
    "configurable": {
        "thread_id": str(uuid.uuid4()),
    }
}
print("Invoking graph...")
graph.invoke({}, config)

print("Checkpointed states:")
states = list(graph.get_state_history(config))
for i, state in enumerate(reversed(states)):
    print(f"State {len(states) - i}: {state}")


mid_checkpoint = states[0]
config_replay = {
    "configurable": {
        "thread_id": config["configurable"]["thread_id"],
        "checkpoint_id": mid_checkpoint.config["configurable"]["checkpoint_id"],
    }
}

result = graph.invoke(None, config_replay)
print("Result from replaying from checkpoint:", result)


#################################

selected_state = states[1]


new_config = graph.update_state(
    selected_state.config,
    values={"override": "This is an override value"}
)

branch_result = graph.invoke(None, new_config)