import sqlite3
from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("database-mcp")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sales.db")

connection = sqlite3.connect(DB_PATH, check_same_thread=False)
# connection = sqlite3.connect("sales.db", check_same_thread=False)

@mcp.tool()
def get_sales(month: str):
    """Get sales for a particular month"""
    try:
        month = month[0].upper() + month[1:].lower()
        cursor = connection.cursor()
        cursor.execute("SELECT revenue FROM sales WHERE month=?", (month,))
        row = cursor.fetchone()
        return {"revenue": row[0] if row else 0}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_total_sales():
    """Get total sales quantum"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(revenue) FROM sales")
        total_sales = cursor.fetchone()[0]
        return {"total sales": total_sales}
    except Exception as e:
        return {"error": str(e)}

if __name__=="__main__":
    mcp.run(transport="stdio")