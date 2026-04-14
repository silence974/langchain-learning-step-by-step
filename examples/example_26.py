from langchain.chat_models import init_chat_model
from langchain.tools import tool
from envdot import load_env
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph

load_env()


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """返回两个整数的和"""
    return a + b


model = init_chat_model("deepseek-reasoner")

tools = [multiply, add]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)


class AssistantState(MessagesState):
    llm_calls: int
    current_action: str
    tool_results: list


def llm_node(state: AssistantState) -> AssistantState:
    response = model_with_tools.invoke(state["messages"])
    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
        "current_action": "llm_reasoning",
    }


def tool_node(state: AssistantState) -> AssistantState:
    last_message = state["messages"][-1]
    tool_messages = []
    new_tool_results = []

    for tool_call in last_message.tool_calls:
        tool = tools_by_name[tool_call["name"]]
        tool_message = tool.invoke(tool_call)
        tool_messages.append(tool_message)
        new_tool_results.append(
            {
                "tool_name": tool_call["name"],
                "args": tool_call["args"],
                "result": tool_message.content,
                "success": tool_message.status == "success",
            }
        )

    return {
        "messages": tool_messages,
        "current_action": "tool_execution",
        "tool_results": state.get("tool_results", []) + new_tool_results,
    }


def should_continue(state: AssistantState):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tool_node"
    return END


workflow = StateGraph(AssistantState)

workflow.add_node("llm_node", llm_node)
workflow.add_node("tool_node", tool_node)

workflow.set_entry_point("llm_node")

workflow.add_conditional_edges(
    "llm_node",
    should_continue,
    {
        "tool_node": "tool_node",
        END: END,
    },
)

workflow.add_edge("tool_node", "llm_node")

agent = workflow.compile()


initial_state = {
    "messages": [
        {
            "role": "user",
            "content": "What is 2 + 3 multiplied by 4?",
        }
    ],
    "llm_calls": 0,
    "current_action": START,
    "tool_results": [],
}

result = agent.invoke(initial_state)
print("Final result:", result)



graph_image = agent.get_graph().draw_ascii()

print(graph_image)


##############################################################

from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

config: RunnableConfig = {
    "configurable": {
        "thread_id": "1",
    },
}

result = graph.invoke(initial_state, config=config)


##############################################################


config = {
    "configurable": {
        "thread_id": "1",
    },
}
current_state = graph.get_state(config=config)

config = {
    "configurable": {
        "thread_id": "1",
    },
}
history = graph.get_state_history(config=config)


from typing import Annotated, TypedDict
from operator import add


class ConversationState(TypedDict):
    messages: Annotated[list, add]
    user_profile: dict
    

def update_user_profile(state: ConversationState, config: RunnableConfig) -> ConversationState:
    return {"user_profile": {"preferences_saved": True}}
    # messages 字段保持不变，仍然可以访问完整历史