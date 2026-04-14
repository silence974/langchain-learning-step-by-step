from langchain.tools import tool
from langchain.agents import create_agent

subagent = create_agent(
    model="deepseek-reasoner",
    tools=[...],
)


@tool("email_agent", description="这是一个电子邮件子代理，负责处理与电子邮件相关的查询。")
def call_subagent(input: str):
    """调用子代理处理输入"""
    response = subagent.invoke(
        {
            "messages": [
                {"role": "user", "content": input}
            ]
        }
    )
    return response["messages"][-1].content

agent = create_agent(
    model="deepseek-reasoner",
    tools=[call_subagent],
    system_prompt="你是一个智能助手，可以根据用户的需求调用不同的子代理来完成任务。"
)