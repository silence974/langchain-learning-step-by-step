from operator import imod
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()  # 加载环境变量


@tool
def get_weather(location: str):
    """获取天气信息"""
    if location == "北京":
        return "北京的天气是晴天，温度25度。"
    elif location == "上海":
        return "上海的天气是多云，温度28度。"
    else:
        return f"{location}的天气信息暂不可用。"


model = init_chat_model("deepseek-reasoner")
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是一个天气助手，可以根据用户提供的地点信息，返回相应的天气信息。"
)

result = agent.invoke(
    {
        "messages": [
            HumanMessage(content="请告诉我北京和上海的天气信息。")
        ]
    }
)

print(result)