from typing import Literal
import json
import math
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Mcp")


# 声明工具1
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# 声明工具2
@mcp.tool()
def query_weather(city_name: str):
    """查询天气"""
    return f"${city_name} is sunny!"


# 声明提示词
@mcp.prompt()
def get_prompt(prompt_theme: Literal["story", "song", "poem"]):
    """获取指定类型主题创作提示词
    prompt_theme: Literal["story", "song", "poem"]
    return: str
    """
    prompt_dict = {
        "story": "你是个很会写童话故事的人，请写一个童话故事",
        "song": "你是个很会写歌曲的人，请写一首歌曲",
        "poem": "你是个很会写诗的人，请写一首诗",
    }
    return f"{prompt_dict[prompt_theme]}"



@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


def main():
     # 启动mcp服务器
    mcp.run(transport="stdio")

if __name__ == "__main__":
    # 启动mcp服务器
   main()


