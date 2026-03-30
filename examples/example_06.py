from langgraph.types import Command
from langchain.tools import tool, ToolRuntime


@tool
def update_user_name(new_name: str, runtime: ToolRuntime) -> Command:
    """更新用户的名字
    
    Args:
        new_name (str): 新的名字
    """
    return Command(
        update={"user_name": new_name},
    )


@tool
def clear_conversation() -> Command:
    """清除当前对话历史"""
    from langchain.messages import RemoveMessage
    from langgraph.graph.message import REMOVE_ALL_MESSAGES
    
    return Command(
        update={
            "messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)],
        }
    )