from envdot import load_env
from langchain.chat_models import init_chat_model

import os

load_env()

model = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url=os.environ.get("DEEPSEEK_API_URL"),
    temperature=0.7,
    timeout=30,
    max_tokens=1000,
)

# 1. 单条消息
response = model.invoke("What is the capital of France?")
print(response)

# 2. 多条消息
conversation = [
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What is the population of Paris?"},
]

response = model.invoke(conversation)
print(response)

# 3. 流式输出

for chunk in model.stream("What is the capital of France?"):
    print(chunk.content, end="", flush=True)
print()

# 4. 批量调用

requests = [
    "What is the capital of France?",
    "What is the population of Paris?",
    "What is the largest city in France?",
]
responses = model.batch(requests)
for i, resp in enumerate(responses):
    print(f"Request {i+1}: {requests[i]}")
    print(f"Response {i+1}: {resp}")
