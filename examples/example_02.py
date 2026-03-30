from envdot import load_env
from langchain_ollama import ChatOllama

import os

load_env()

model = ChatOllama(
    model="deepseek-r1:8b",
    temperature=0,
    base_url="http://192.168.31.57:11434",
)

print(model.profile)

resp = model.invoke("What is the capital of France?")
print(resp)