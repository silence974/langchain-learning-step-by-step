from envdot import load_env
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage

import os

load_env()

model = init_chat_model(
    model="deepseek-reasoner",
    model_provider="deepseek",
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url=os.environ.get("DEEPSEEK_API_URL"),
    temperature=0.7,
    timeout=30,
    max_tokens=1000,
)

agent = create_agent(model=model, system_prompt="你是一个知识渊博的助手，能够回答各种问题。")

resp = agent.invoke(HumanMessage("你好，请告诉我你的名字"))
print(resp)