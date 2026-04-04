from langchain.tools import tool, ToolRuntime

from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from envdot import load_env
load_env()

class CustomState(AgentState):
    user_name: str


@tool
def greet(runtime: ToolRuntime) -> str:
    """一个简单的工具函数，用于根据用户名称生成问候语"""
    user_name = runtime.state["user_name"]
    return f"Hello, {user_name}!"

model = init_chat_model(
    model="deepseek-reasoner",
    model_provider="deepseek",
)

agent = create_agent(
    model,
    tools=[greet],
    state_schema=CustomState,
    checkpointer=InMemorySaver(),
)

# result = agent.invoke({
#     "messages": [
#         {"role": "user", "content": "向用户问好"},
#     ],
#     "user_name": "Alice",
# }, {
#     "configurable": {
#         "thread_id": "user_greeting_thread",
#     }
# })

# print(result)


# from pydantic import BaseModel, Field
# from langchain.agents.structured_output import ProviderStrategy

# class MeetingAction(BaseModel):
#     topic: str = Field(..., description="会议主题")
#     participants: list = Field(..., description="会议参与者列表")
#     action_items: list = Field(..., description="会议行动项列表")
#     deadline: str = Field(..., description="行动项截止日期")
    
# meeting_agent = create_agent(
#     model,
#     response_format=ProviderStrategy(MeetingAction)
# )

# resp = meeting_agent.invoke({
#     "messages": [
#         {"role": "user", "content": "从会议纪要中提取：项目评审会议，张三和李四参加，需要完成代码审查，截止下周三"}
#     ]
# })

# meeting_data = resp["structured_response"]
# print(meeting_data)


from langchain.agents.structured_output import ProviderStrategy

contact_info_schema = {
    "type": "object",
    "description": "Contract information for a persion.",
    "properties": {
        "name": {"type": "string", "description": "用户名"},
        "email": {"type": "string", "description": "用户的邮箱地址"},
        "phone": {"type": "string", "description": "用户的手机号"},
    },
    "required": ["name", "email", "phone"]
}

contact_agent = create_agent(
    model,
    response_format=ProviderStrategy(contact_info_schema)
)

from typing import Union, Literal, List
from pydantic import BaseModel, Field

class EmailContact(BaseModel):
    email: str
    type: Literal["email"] = "email"
    
class PhoneContact(BaseModel):
    phone: str
    type: Literal["phone"] = "phone"

ContactUnion = Union[EmailContact, PhoneContact]

contact_agent = create_agent(
    model,
    response_format=ProviderStrategy(ContactUnion)
)

class Address(BaseModel):
    street: str
    city: str
    country: str
    
class CompanyContact(BaseModel):
    name: str
    address: Address
    employees: List[str]
    founded_year: int

agent = create_agent(
    model,
    response_format=ProviderStrategy(CompanyContact)
)