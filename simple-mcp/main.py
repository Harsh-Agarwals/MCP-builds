from mcp.server.fastmcp import FastMCP
import math

mcp = FastMCP(name="SimpleMCP")

# Defining tools
# addition tool
@mcp.tool()
def get_addition(a: int, b: int) -> int:
    """addition of two integers"""
    return int(a+b)

# subtration tool
@mcp.tool()
def get_subtraction(a: int, b: int) -> int:
    """subtraction of two integers"""
    return int(a-b)

# factorial tool
@mcp.tool()
def get_factorial(a: int) -> int:
    """factorial of an integer"""
    return int(math.factorial(a))

# log tool
@mcp.tool()
def get_log(a: int) -> float:
    """logarithm of an integer"""
    return round(math.log(a),2)

# Defining resources
@mcp.resource("greetings://{name}")
def get_greeting(name: str) -> str:
    """greet a person"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="stdio")