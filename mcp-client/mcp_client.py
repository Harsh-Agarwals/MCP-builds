from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import sys
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class MCPClient:
    def __init__(self) -> None:
        pass

    async def connect_to_server(self, path_to_server_script: str):
        """
        Connect to MCP server

        Args:
            path_to_server_script: path to MCP server file (.py or .js)
        """
        is_python = path_to_server_script.endswith(".py")
        is_js = path_to_server_script.endswith(".js")

        if not is_python or not is_js:
            raise ValueError("Server script must be .py or .js")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[path_to_server_script],
            env=None,
        )
        pass

    async def process_query(self):
        pass

    async def chat_loop(self):
        pass

async def main():
    pass

if __name__=="__main__":
    asyncio.run(main())