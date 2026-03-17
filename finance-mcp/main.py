from mcp.server.fastmcp import FastMCP
import yfinance as yf
import logging
import os
from pathlib import Path

mcp = FastMCP("finance-mcp")
LOG_DIR = os.path.join(Path.cwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "finance_mcp.log"),
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s"
)
print(os.path.join(LOG_DIR, "finance_mcp.log"))

def fetch_price(symbol: str):
    try:
        logging.error("TEST LOG WORKING")
        symbol = symbol.upper()
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            closing_price = data['Close'].values[-1]
            return {"closing_price": closing_price}
        else:
            stock_price = ticker.fast_info.get("lastPrice")
            if stock_price is not None:
                return {"closing_price": stock_price}
            logging.error(f"Invalid stock symbol: {symbol}")
            return {"closing_price": -1}
    except Exception:
        logging.exception(f"Error fetching stock price for {symbol}")
        return {"closing_price": -1}

@mcp.tool()
def get_stock_price(symbol: str):
    try:
        stock_price = fetch_price(symbol=symbol)
        return stock_price
    except Exception as e:
        logging.exception(f"Unhandled error in get_stock_price for {symbol}")
        return {"error": str(e)}

@mcp.tool()
def get_stock_history(symbol: str, period: str):
    try:
        symbol = symbol.upper()
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        if data.empty:
            return {"error": f"No data found for symbol {symbol} for period {period}. Try one of: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max for period."}
        return {
            "symbol": symbol,
            "period": period,
            "data": data.reset_index().to_dict(orient="records")
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def compare_stock_price(symbol1: str, symbol2: str):
    try:
        symbol1 = symbol1.upper()
        symbol2 = symbol2.upper()
        price1 = fetch_price(symbol=symbol1)['closing_price']
        price2 = fetch_price(symbol=symbol2)['closing_price']
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
    price = fetch_price(symbol=symbol)['closing_price']
    if price<0:
        return f"{symbol} symbol is incorrect"
    else:
        return f"The price for stock {symbol} is {price:.2f}"

if __name__=="__main__":
    mcp.run(transport="stdio")