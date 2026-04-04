from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model

from envdot import load_env
load_env()

model = init_chat_model(
    model="deepseek-reasoner",
    model_provider="deepseek",
)

agent = create_agent(
    model,
    # tools=["python_repl"],
    checkpointer=InMemorySaver(),
)

resp = agent.invoke({
    "messages": [
        {"role": "user", "content": "请计算一下 2 的 10 次方是多少？"},
    ],
}, {
    "configurable": {
        "thread_id": "1",
    }
})

print(resp)