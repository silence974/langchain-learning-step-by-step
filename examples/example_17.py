from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()  # 加载环境变量

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "uv",
                "args": ["run", "example_15.py"],
            },
            "weather": {
                "transport": "streamable-http",
                "url": "http://localhost:8000/mcp",
            }
        }
    )


    tools = await client.get_tools()
    agent = create_agent(
        model="deepseek-reasoner",
        tools=tools,
    )

    math_response = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": "请计算 5 + 3 和 4 * 2 的结果。"}
            ]
        }
    )
    weather_response = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": "请告诉我北京和上海的天气信息。"}
            ]
        }
    )

    print("Math Response:", math_response)
    print("Weather Response:", weather_response)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    
    
# from langchain_mcp_adapters.client import load_mcp_tools

# client = MultiServerMCPClient({...})
# async with client.session("math") as session:
#     tools = await load_mcp_tools(session)