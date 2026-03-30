from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

# 1. class

@dataclass
class UserContext:
    user_id: str
    
# 2. tool

@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """获取用户的账户信息"""
    user_id = runtime.context.user_id
    return f"用户 {user_id} 的账户信息：余额100元，积分200分"

# 3. create

# agent = create_agent(
#     model=model,
#     tools = [get_account_info],
#     context_schema=UserContext,
#     system_prompt="你是一个知识渊博的助手，能够回答各种问题。",
# )


# 4. use

# resp = agent.invoke(
#     HumanMessage(content="请告诉我我的账户信息"),
#     context=UserContext(user_id="12345"),
# )