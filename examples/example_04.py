## 1. load

from langchain.messages import HumanMessage, AIMessage, SystemMessage

## 2. create

# 创建系统消息 - 设置模型行为

system_msg = SystemMessage(content="你是一个知识渊博的助手，能够回答各种问题。")

# 创建用户消息 - 用户输入

human_msg = HumanMessage(content="你好，请告诉我你的名字")

# 创建助手消息 - 模型答复

ai_msg = AIMessage(content="你好！我是一个AI助手，没有名字，但我很高兴为你提供帮助！")

## 3. use

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from envdot import load_env

load_env()

model = init_chat_model(
    model="deepseek-reasoner",
    model_provider="deepseek",
)

messages = [
    SystemMessage(content="你是一个知识渊博的助手，能够回答各种问题。"),
    HumanMessage(content="你好，请告诉我你的名字"),
]

resp = model.invoke(messages)
print(resp)