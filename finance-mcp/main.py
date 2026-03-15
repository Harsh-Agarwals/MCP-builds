from operator import ge
from mcp.server.fastmcp import FastMCP
import yfinance as yf
import pandas as pd

mcp = FastMCP("finance-mcp")

@mcp.tool()
def get_stock_price(symbol: str):
    try:
        symbol = symbol.upper()
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        closing_price = data['Close'].values[-1]
        if not data.empty:
            return {"closing_price": closing_price}
        else:
            stock_info = ticker.info
            stock_price = stock_info['regularMarketPreviousClose']
            if stock_price is not None:
                return {"closing_price": stock_price}
            else:
                return {"closing_price": -1}
    except Exception as e:
        return {"closing_price": -1}

@mcp.tool()
def get_stock_history(symbol: str, period: str):
    try:
        symbol = symbol.upper()
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        if data.empty:
            return {"error": f"No data found for symbol {symbol} for period {period}. Try one of: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max for period."}
        csv_data = data.to_csv()
        return csv_data
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def compare_stock_price(symbol1: str, symbol2: str):
    try:
        symbol1 = symbol1.upper()
        symbol2 = symbol2.upper()
        price1 = get_stock_price(symbol1)['closing_price']
        price2 = get_stock_price(symbol2)['closing_price']
        if price1 == -1 or price2 == -1:
            return "One or more symbol is incorrect"
        if price1 > price2:
            result = f"{symbol1} (${price1:.2f}) is higher than {symbol2} (${price2:.2f})."
        elif price1 < price2:
            result = f"{symbol1} (${price1:.2f}) is lower than {symbol2} (${price2:.2f})."
        else:
            result = f"Both {symbol1} and {symbol2} have the same price (${price1:.2f})."
        return result
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("stock://{symbol}")
def stock_resource(symbol: str):
    price = get_stock_price(symbol)['closing_price']
    if price<0:
        return f"{symbol} symbol is incorrect"
    else:
        return f"The price for stock {symbol} is {price:.2f}"

if __name__=="__main__":
    mcp.run(transport="stdio")