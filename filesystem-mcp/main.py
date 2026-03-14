from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="filesystem-mcp")

# @mcp.tool()
# def get_files_list() -> 

if __name__=="__main__":
    mcp.run(transport="stdio")