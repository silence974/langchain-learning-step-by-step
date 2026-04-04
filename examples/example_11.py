from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool, ToolRuntime
from envdot import load_env
load_env()

model = init_chat_model(
    model="deepseek-reasoner",
    model_provider="deepseek",
)

hitl_middleware = HumanInTheLoopMiddleware(
    interrupt_on={
        "write_file": True, # 当模型调用 write_file 工具时，触发 HITL 中断，等待用户批准
        "execute_sql": {
            "allowed_decisions": ["approve", "reject"], # 不允许编辑
        },
        "read_data": False, # 自动批准
    },
    description_prefix="工具执行待审核"
)

agent = create_agent(
    model,
    tools=[write_file, execute_sql, read_data],
    middleware=[hitl_middleware],
    checkpointer=InMemorySaver(),  # 必需，支持中断和恢复
)




from langgraph.types import Command

# 必需，提供线程 IO 以支持中断和恢复
config = {
    "configurable": {
        "thread_id": "file_operations_thread",
    }
}

result = agent.invoke({
    "messages": [
        {"role": "user", "content": "请创建一个文件，并写入一些内容"},
    ],
}, config)

if "__interrupt__" in result:
    interrupt = result["__interrupt__"][0]
    print(f"需要审核的操作: {interrupt['value']}")
    
    human_decision = {
        "decisions": [
            {
                "type": "reject",
                "message": reason,
            }
        ]
    }
    
    final_result = agent.invoke(
        Command(resume=human_decision),
        config=config,
    )
