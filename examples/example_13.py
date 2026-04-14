from langchain.agents.middleware import AgentMiddleware, AgentState, ModelRequest, ModelResponse
from langchain.agents.middleware.types import ToolCallRequest
from langchain_core.messages import ToolMessage
from typing import Any, Callable


class CoreMiddlewareDemo(AgentMiddleware):
    def __init__(self, log_level: str = "INFO"):
        self.log_level = log_level
        
    def before_agent(self, state: AgentState, runtime: Any) -> dict[str, Any] | None:
        messages = state.get("messages", [])
        if len(messages) == 0:
            print(f"[{self.log_level}] 没有初始消息.")
            return None
        return {
            "context": {
                "message_count": len(messages),
            }
        }

    def after_agent(self, state: AgentState, runtime: Any) -> dict[str, Any] | None:
        print(f"[{self.log_level}] 代理完成执行.")
        return None
    
    def before_model(self, state: AgentState, runtime: Any) -> dict[str, Any] | None:
        print(f"[{self.log_level}] 模型请求即将发送.")
        return None
    
    def after_model(self, state: AgentState, runtime: Any) -> dict[str, Any] | None:
        print(f"[{self.log_level}] 模型请求已完成.")
        return None
    
    def wrap_model_call(self, request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
        response = handler(request)
        print(f"[{self.log_level}] 模型调用已包装.")
        return response