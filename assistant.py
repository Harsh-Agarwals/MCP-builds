# Using both filesystem and database MCP to get and compare forecast values with real sales values
# AI assistant will read forecasted.txt doc, read sales db data and compare results

# We'll use filesystem-MCP for reading files, database-MCP for reading database and LLM for comparison

import asyncio
from contextlib import AsyncExitStack
from typing import Optional
from anthropic import Anthropic
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import os
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("CLAUDE_API_KEY")

filesystem_server = StdioServerParameters(
    command="python",
    args=["filesystem-mcp/main.py"],
    env=None
)

database_server = StdioServerParameters(
    command="python",
    args=["database-mcp/main.py"],
    env=None
)

class MCPClient:
    def __init__(self) -> None:
        self.anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.exit_stack = AsyncExitStack()
        self.session: Optional[ClientSession] = None

    async def connect_to_servers(self):
        try:
            fs_transport = await self.exit_stack.enter_async_context(stdio_client(filesystem_server))
            db_transport = await self.exit_stack.enter_async_context(stdio_client(database_server))

            fs_read, fs_write = fs_transport
            db_read, db_write = db_transport
        
            self.fs_session = await self.exit_stack.enter_async_context(ClientSession(fs_read, fs_write))
            self.db_session = await self.exit_stack.enter_async_context(ClientSession(db_read, db_write))

            await self.fs_session.initialize()
            await self.db_session.initialize()

            fs_tools_list = await self.fs_session.list_tools()
            db_tools_list = await self.db_session.list_tools()

            fs_tools = fs_tools_list.tools
            db_tools = db_tools_list.tools

            print(f"Connected to Filesystem and Database servers with tools: {fs_tools}, {db_tools}")
        except Exception as e:
            print(f"error: {e}")

    async def clean_sessions(self):
        await self.exit_stack.aclose()

    async def process_query(self, query):

        messages = [{
            'role': 'user',
            'content': query
        }]

        fs_tools_list = await self.fs_session.list_tools()
        db_tools_list = await self.db_session.list_tools()

        fs_tools = fs_tools_list.tools
        db_tools = db_tools_list.tools

        available_tools = [{
            'name': f"fs_{tool.name}",
            'description': tool.description,
            'input_schema': tool.inputSchema
        } for tool in fs_tools] + [{
            'name': f"db_{tool.name}",
            'description': tool.description,
            'input_schema': tool.inputSchema
        } for tool in db_tools]

        llm_parsing = self.anthropic.messages.create(
            max_tokens=512,
            messages=messages,
            model="claude-sonnet-4-20250514",
            tools=available_tools
        )

        steps = llm_parsing.content
        print(steps)

        result_steps = []
        # llm_context = []

        for step in steps:
            print(step)
            if step.type == "text":
                print('text')
                result_steps.append(step.text)
                # llm_context.append(step)
            elif step.type == "tool_use":
                print('tool-use')
                tool_name, tool_params = step.name, step.input
                result_steps.append(f"Using tool {tool_name} with args {tool_params}")
                print(result_steps)
                if tool_name.startswith('fs'):
                    tool_name = tool_name[3:]
                    tool_result = await self.fs_session.call_tool(name=tool_name, arguments=tool_params)
                elif tool_name.startswith('db'):
                    tool_name = tool_name[3:]
                    tool_result = await self.db_session.call_tool(name=tool_name, arguments=tool_params)
                print(tool_result)
                # llm_context.append(step)
                messages.append({
                    'role': 'assistant',
                    'content': [step]
                })
                messages.append({
                    'role': 'user',
                    'content': [{
                        'type': "tool_result",
                        'tool_use_id': step.id,
                        'content': tool_result.content
                    }]
                })
        print(messages)
        response = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=messages
        )
        print(response.content)
        result_steps.append(response.content[0].text)

        return '\n'.join(result_steps)

async def main():
    client = MCPClient()
    try:
        await client.connect_to_servers()
        query = input("Query: ").strip()
        response = await client.process_query(query=query)

        print(f"\n{response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.clean_sessions()

if __name__=="__main__":
    asyncio.run(main())