from dataclasses import dataclass
from langchain.agents import create_agent

@dataclass
class Context:
    user_name: str
    
    
agent = create_agent(
    model="gpt-3.5-turbo",
    tools=[],
    context_schema=Context,
)

agent.invoke({
    "messages": [
        {"role": "user", "content": "请问我的名字是什么？"}
    ]
}, context=Context(user_name="Alice"))


from langchain.tools import tool, ToolRuntime


@tool
def fetch_user_email_preferences(runtime: ToolRuntime[Context]) -> str:
    user_name = runtime.context.user_name
    # 模拟获取用户的邮件偏好设置
    if user_name == "Alice":
        return "Alice的邮件偏好设置是：每天接收一次总结邮件。"
    else:
        return f"{user_name}的邮件偏好设置未知。"
    
    
from langchain.agents.middleware import dynamic_prompt, ModelRequest

@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest):
    user_name = request.runtime.context.user_name
    return f"你是一个智能助手，正在与用户 {user_name} 进行对话。请根据用户的名字提供个性化的回复。"

