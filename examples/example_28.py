from envdot import load_env
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.memory import InMemoryStore
from langchain_core.runnables import RunnableConfig
from typing import Annotated, TypedDict
import operator
import uuid


load_env()
store = InMemoryStore()


class ChatState(TypedDict):
    messages: Annotated[list, operator.add]
    user_preferences: dict
    conversation_summary: str


def process_message(state: ChatState, config: RunnableConfig):
    latest_message = state["messages"][-1]
    user_id = config["configurable"]["thread_id"]
    preferences = store.search((user_id, "preferences"))
    preference_text = "未找到偏好信息"

    if preferences:
        latest_preferences = preferences[-1].dict()["value"]
        preference_text = f"已记录偏好：{latest_preferences}"
    
    return {
        "messages": [{
            "role": "assistant",
            "content": f"收到您的消息：{latest_message['content']} {preference_text}",
        }],
        "user_preferences": preferences[-1].dict()["value"] if preferences else {},
    }


workflow = StateGraph(ChatState)
workflow.add_node("process_message", process_message)
workflow.add_edge(START, "process_message")
workflow.add_edge("process_message", END)

config = {
    "configurable": {
        "thread_id": str(uuid.uuid4()),
    }
}
store.put(
    (config["configurable"]["thread_id"], "preferences"),
    str(uuid.uuid4()),
    {"favorite_genre": "science fiction"},
)
initial_state = {
    "messages": [
        {
            "role": "user",
            "content": "Hello, I like science fiction movies.",
        }
    ],
    "user_preferences": {},
    "conversation_summary": "",
}

with SqliteSaver.from_conn_string("chatbot.db") as checkpointer:
    graph = workflow.compile(checkpointer=checkpointer)
    result = graph.invoke(initial_state, config)

print("Final result:", result)
