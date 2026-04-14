from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")


@mcp.tool()
async def get_weather(city: str) -> str:
    """返回指定城市的天气信息"""
    # 模拟获取天气信息
    weather_info = {
        "北京": "晴，25°C",
        "上海": "多云，22°C",
        "广州": "雨，28°C",
    }
    return weather_info.get(city, f"{city}的天气信息未知。")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")