import sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("database-mcp")
connection = sqlite3.connect("sales.db", check_same_thread=False)

@mcp.tool()
def get_sales(month: str):
    """Get sales for a particular month"""
    month = month[0].upper() + month[1:].lower()
    cursor = connection.cursor()
    cursor.execute("SELECT revenue FROM sales WHERE month=?", (month,))
    row = cursor.fetchone()
    return {"revenue": row[0] if row else 0}

@mcp.tool()
def get_total_sales():
    """Get total sales quantum"""
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(revenue) FROM sales")
    total_sales = cursor.fetchone()[0]
    return {"total sales": total_sales}

if __name__=="__main__":
    mcp.run(transport="stdio")