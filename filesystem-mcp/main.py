from fileinput import filename
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP(name="filesystem-mcp")

BASE_DIR = os.path.abspath(".")
def resolve_path(folder_name: str):
    folder_path = os.path.abspath(os.path.join(BASE_DIR, folder_name))

    if not folder_path.startswith(BASE_DIR):
        raise ValueError("Incorrect path")
    
    if not os.path.isdir(folder_path):
        raise ValueError("The folder does not exists.")

    return folder_path

@mcp.tool()
def get_files_list(folder_name: str):
    """get list of all the files inside folder folder_name"""
    try:
        folder_path = resolve_path(folder_name)
        return {"files": os.listdir(path=folder_path)}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def read_file(file_name: str, folder_name: str):
    """read file file_name inside folder folder_name"""
    try:
        folder_path = resolve_path(folder_name)
        if file_name in os.listdir(path=folder_path):
            with open(os.path.join(folder_path, file_name), 'r') as f:
                return {"content": f.read()}
        else:
            return {"error": f"The file Does Not Exists inside folder {folder_path}"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_file(file_name: str, folder_name: str):
    """search file file_name inside folder folder_name"""
    try:
        folder_path = resolve_path(folder_name)
        file_list = os.listdir(path=folder_path)
        file = bool(file_name in file_list)
        return {"result": f"{file_name} is available in folder {folder_path}"} if file==True else {"result": f"{file_name} is not available in folder {folder_path}"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_file_by_type(file_type: str, folder_name: str):
    try:
        folder_path = resolve_path(folder_name)
        file_list = os.listdir(path=folder_path)
        files = list(filter(lambda x: x.endswith(file_type), file_list))
        if len(files) == 0:
            return {"error": f"No {file_type} filetype found in {folder_path}"}
        return {"result": files} if len(files) == 1 else {"results": files}
    except Exception as e:
        return {"error": str(e)}

@mcp.prompt()
def summarize_folder_structure(folder_name: str):
    folder_path = resolve_path(folder_name)
    """Prompt template to help LLM analyse folder and files inside"""
    return f"Please analyze the directory '{folder_path}'. List the main components and explain the technical purpose of this project based on its file names."

if __name__=="__main__":
    mcp.run(transport="stdio")