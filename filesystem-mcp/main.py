from fileinput import filename
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP(name="filesystem-mcp")

@mcp.tool()
def get_files_list(folder_name: str):
    """get list of all the files inside folder folder_name"""
    if folder_name in os.listdir():
        return {"files": os.listdir(path=folder_name)}
    else:
        return {"error": "The folder Does Not Exists"}

@mcp.tool()
def read_file(file_name: str, folder_name: str):
    """read file file_name inside folder folder_name"""
    if folder_name in os.listdir():
        if file_name in os.listdir(path=folder_name):
            with open(os.path.join(folder_name, file_name), 'r') as f:
                return {"content": f.read()}
        else:
            return {"error": f"The file Does Not Exists inside folder {folder_name}"}
    else:
        return {"error": "The folder Does Not Exists"}

@mcp.tool()
def search_file(file_name: str, folder_name: str):
    """search file file_name inside folder folder_name"""
    if folder_name in os.listdir():
        file_list = os.listdir(path=folder_name)
        files = list(filter(lambda x: x==file_name, file_list))
        if len(files) == 0:
            return {"error": f"No {file_name} found in {folder_name}"}
        return {"results": files}
    else:
        return {"error": "The folder Does Not Exists"}

if __name__=="__main__":
    mcp.run(transport="stdio")