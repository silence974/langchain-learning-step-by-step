from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """返回两个整数的和"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """返回两个整数的积"""
    return a * b


if __name__ == "__main__":
    mcp.run(transport="stdio")