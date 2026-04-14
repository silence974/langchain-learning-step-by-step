from deepagents import create_deep_agent, CompiledSubAgent
from langchain.agents import create_agent

custom_graph = create_agent(
    model="deepseek-reasoner",
    tools=[...],
    system_prompt="你是一个专业的数据分析师，擅长处理复杂的数据分析任务。"
)

custom_subagent = CompiledSubAgent(
    name="custom_subagent",
    description="这是一个自定义子代理，负责处理特定的数据分析任务。",
    runnable=custom_graph,
)

subagents = [custom_subagent]

tagent = create_deep_agent(
    model="deepseek-reasoner",
    subagents=subagents,
    system_prompt="你是一个智能助手，可以根据用户的需求调用不同的子代理来完成任务。"
)