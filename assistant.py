# Using both filesystem and database MCP to get and compare forecast values with real sales values
# AI assistant will read forecasted.txt doc, read sales db data and compare results

# We'll use filesystem-MCP for reading files, database-MCP for reading database and LLM for comparison

from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
from mcp import StdioServerParameters

fs_params = StdioServerParameters(
    command="/Users/harshagarwal/Desktop/mcp-builds/venv/bin/python",
    args=["filesystem-mcp/main.py"]
)

db_params = StdioServerParameters(
    command="/Users/harshagarwal/Desktop/mcp-builds/venv/bin/python",
    args=["database-mcp/main.py"]
)

print(fs_params)