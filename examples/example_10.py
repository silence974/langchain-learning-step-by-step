from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from envdot import load_env
load_env()

model = init_chat_model(
    model="deepseek-reasoner",
    model_provider="deepseek",
)

agent = create_agent(
    model,
    middleware=[SummarizationMiddleware(), HumanInTheLoopMiddleware()],
)



model = init_chat_model(
    model="deepseek-reasoner",
    model_provider="deepseek",
)

summarization = SummarizationMiddleware(
    model=model,
    trigger=[("fraction", 0.8)],
    keep=("fraction", 0.3),
)

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

