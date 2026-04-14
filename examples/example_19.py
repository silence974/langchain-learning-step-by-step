from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from deepagents.backends import FilesystemBackend
from dotenv import load_dotenv
load_dotenv()  # 加载环境变量


model = init_chat_model("deepseek-reasoner")

@tool
def get_weather(location: str):
    """获取天气信息"""
    if location == "北京":
        return "北京的天气是晴天，温度25度。"
    elif location == "上海":
        return "上海的天气是多云，温度28度。"
    else:
        return f"{location}的天气信息暂不可用。"

agent = create_deep_agent(
    model=model,
    backend=FilesystemBackend(root_dir="./agent_data", virtual_mode=True),
    subagents=[
        {
            "name": "weather_agent",
            "description": "天气子代理，负责处理与天气相关的查询。",
            "tools": [get_weather],
            "system_prompt": "你是一个天气助手，可以根据用户提供的地点信息，返回相应的天气信息。"
        }
    ],
    system_prompt="你是一个智能助手，可以根据用户的需求调用不同的子代理来完成任务。"
)

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "请告诉我北京和上海的天气信息。"}
        ]
    }
)

print(result)