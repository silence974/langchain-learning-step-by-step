import os
from typing import Literal
from deepagents import create_deep_agent

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["technology", "health", "finance", "sports", "entertainment"] = "technology",
    include_raw_content: bool = False
):
    """模拟一个互联网搜索工具，根据查询和主题返回相关结果"""
    # 这里我们只是模拟返回一些结果，实际应用中可以调用真实的搜索API
    results = [f"Result {i+1} for '{query}' in {topic}" for i in range(max_results)]
    if include_raw_content:
        results = [f"{result} - Raw content for {result}" for result in results]
    return results


research_subagent = {
    "name": "research_agent",
    "description": "这是一个研究子代理，负责处理与研究相关的查询。",
    "tools": [internet_search],
    "model": "deepseek-reasoner",
}
subagents = [research_subagent]

tagent = create_deep_agent(
    model="deepseek-reasoner",
    subagents=subagents,
    system_prompt="你是一个智能助手，可以根据用户的需求调用不同的子代理来完成任务。"
)