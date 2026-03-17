import os
from pathlib import Path
from xml.etree.ElementTree import TreeBuilder
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import logging

load_dotenv()
mcp = FastMCP("weatherMcp")
OPENWEATHER_API = os.getenv("OPENWEATHER_API_KEY")
LOG_DIR = os.path.join(Path.cwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging_filename = os.path.join(LOG_DIR, "weather_mcp_log.log")
# if not os.path.exists(logging_filename):
#     with open(logging_filename, 'w') as f:
#         f.write("Logs for weather MCP...")
logging.basicConfig(
    filename=logging_filename,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    force=True
)
logger = logging.getLogger()

def get_current_weather(city: str):
    try:
        weather_api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API}"
        data = requests.get(weather_api)
        weather_data = data.json()
        return weather_data
    except Exception as e:
        logger.error(f"Error {str(e)}")
        return None

def format_alert(json_data: dict):
    try:
        return f"""
        'weather type': {json_data['weather'][0]['description']},
        'temperature': {json_data['main']['temp']},
        'humidity': {json_data['main']['humidity']},
        'wind speed': {json_data['wind']['speed']}
        """
    except Exception as e:
        logger.error(f"Error {str(e)}")
        return None

@mcp.tool()
def get_alerts(city: str):
    try: 
        city = city.lower()
        weather_data = get_current_weather(city)
        return format_alert(weather_data)
    except Exception as e:
        logger.error(f"Error {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def get_weather(city: str, variable: str):
    try: 
        city = city.lower()
        variable = variable.lower()
        weather_data = get_current_weather(city)
        weather = weather_data['main'] | weather_data['wind']
        return {"ctiy": city, f"{variable}": str(weather[variable])}
    except Exception as e:
        logger.error(f"Error {str(e)}")
        return {"error": str(e)}

if __name__=="__main__":
    mcp.run(transport="stdio")