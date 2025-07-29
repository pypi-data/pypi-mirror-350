# weather_sse.py
from mcp.server.fastmcp import FastMCP
import random
 
# 创建MCP服务器实例，指定端口
mcp = FastMCP("Weather Service", port=8000)
 
# 模拟的天气数据
weather_data = {
    "New York": {"temp": range(10, 25), "conditions": ["sunny", "cloudy", "rainy"]},
    "London": {"temp": range(5, 20), "conditions": ["cloudy", "rainy", "foggy"]},
    "Tokyo": {"temp": range(15, 30), "conditions": ["sunny", "cloudy", "humid"]},
    "Sydney": {"temp": range(20, 35), "conditions": ["sunny", "clear", "hot"]},
}
 
@mcp.tool()
def get_weather(city: str) -> dict:
    """获取指定城市的当前天气"""
    if city not in weather_data:
        return {"error": f"无法找到城市 {city} 的天气数据"}
    
    data = weather_data[city]
    temp = random.choice(list(data["temp"]))
    condition = random.choice(data["conditions"])
    
    return {
        "city": city,
        "temperature": temp,
        "condition": condition,
        "unit": "celsius"
    }
 
@mcp.resource("weather://cities")
def get_available_cities() -> list:
    """获取所有可用的城市列表"""
    return list(weather_data.keys())
 
@mcp.resource("weather://forecast/{city}")
def get_forecast(city: str) -> dict:
    """获取指定城市的天气预报资源"""
    if city not in weather_data:
        return {"error": f"无法找到城市 {city} 的天气预报"}
    
    forecast = []
    for i in range(5):  # 5天预报
        data = weather_data[city]
        temp = random.choice(list(data["temp"]))
        condition = random.choice(data["conditions"])
        forecast.append({
            "day": i + 1,
            "temperature": temp,
            "condition": condition
        })
    
    return {
        "city": city,
        "forecast": forecast,
        "unit": "celsius"
    }
 
if __name__ == "__main__":
    # 使用SSE传输方式启动服务器
    mcp.run(transport="sse")