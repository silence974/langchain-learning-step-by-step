from langchain.agents.middleware import PIIMiddleware
from langchain.agents import create_agent


agent = create_agent(
    model,
    tools=[write_file, execute_sql, read_data],
    middleware=[
        PIIMiddleware(
            "email", strategy="redact",
        )
    ],
)

PIIMiddleware("api_key", detector=r"sk-[a-zA-Z0-9]{32,}", strategy="block")


PIIMiddleware("email", strategy="redact", apply_to_input=True, apply_to_output=True, apply_to_tool_results=True)


from langchain.agents.middleware import TodoListMiddleware, LLMToolSelectorMiddleware


LLMToolSelectorMiddleware(
    model=model,
    max_tools=5,
    always_include=["search"]
)

