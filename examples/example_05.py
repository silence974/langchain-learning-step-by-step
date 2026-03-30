from langchain.tools import tool

@tool
def search_web(query: str) -> str:
    """在网上搜索信息
    
    Args:
        query (str): 搜索查询关键词
    """
    return f"搜索结果：{query} 的相关信息"


@tool
def get_weather(location: str) -> str:
    """获取天气信息
    
    Args:
        location (str): 位置名称
    """
    return f"{location} 的天气是晴朗，温度25摄氏度"


from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from envdot import load_env
load_env()

model = init_chat_model(
    model="deepseek-reasoner",
    model_provider="deepseek",
)

tools = [search_web, get_weather]

agent = create_agent(
    model=model,
    system_prompt="你是一个知识渊博的助手，能够回答各种问题。",
    tools=tools,
)

resp = agent.invoke(HumanMessage("请告诉我北京的天气，并搜索一下最新的科技新闻"))
print(resp)