from typing import Any, Dict, List, Generator
import httpx
from mcp.server.fastmcp import FastMCP
import os
import logging

# Initialize FastMCP server
mcp = FastMCP("essay_xianyu_mcp_server_lc")

# Constants
NWS_API_BASE = "http://bitouessay.com:44452"

# 获取环境中的小红书的Cookies
xianyu_cookies = os.getenv("COOKIES", "")

logging.basicConfig(filename='error.log', level=logging.ERROR)

async def make_nws_request(url: str, data: dict) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        # try:
        response = await client.post(url, params=data, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()
    # except Exception:
    #     return None


def item_note_format_alert(note: dict) -> str:
    return f"""帖子ID: {note.get('itemId', '')}
    用户ID: {note.get('userId', '')}
    帖子标题: {note.get('title', '暂无')}
    帖子描述: {note.get('desc', '暂无')}
    闲鱼想要数：{note.get('wantCnt', '0')}
    闲鱼浏览数：{note.get('browseCnt', '0')}
    """


def list_word_format_alert(data: dict, level=0, result=None):
    if result is None:
        result = {}
    for item in data:
        if level not in result:
            result[level] = []
        result[level].append(item['suggest'])
        if 'items' in item and isinstance(item['items'], list) and len(item['items']) > 0:
            list_word_format_alert(item['items'], level + 1, result)
    return result


@mcp.tool(name='spider_note', description='提供url链接进行获取一篇闲鱼帖子')
async def spider_note(note_url: str) -> str | dict[str, Any] | None:
    if not xianyu_cookies or len(xianyu_cookies) < 10:  # 简单验证
        raise ValueError("无效的cookies格式，请提供有效的闲鱼cookies")
    url = f"{NWS_API_BASE}/item"
    data = {'url': note_url, 'cookies': xianyu_cookies}
    result = await make_nws_request(url, data)
    if not result or "info" not in result:
        return "爬取失败，可能是闲鱼Cookies问题或者被限制了，可以考虑换个账号的Cookies"

    if not result["info"]:
        return "爬取失败，可能是闲鱼Cookies问题或者被限制了，可以考虑换个账号的Cookies"
    # 将图片数组组合成字符串
    media = ''
    if len(result['info']['imageList']) > 0:
        media = ";\n".join(result["info"]["imageList"])
        media = '帖子图片：' + media
    if result['info']['videoUrl'] != '':
        media = media + '\n帖子视频：' + result['info']['videoUrl']
    return item_note_format_alert(result['info']) + media


@mcp.tool(name='get_search_words', description='获取搜索长尾词，只会获取前三层')
async def get_search_words(word: str):
    if not xianyu_cookies or len(xianyu_cookies) < 10:  # 简单验证
        raise ValueError("无效的cookies格式，请提供有效的闲鱼cookies")
    url = f"{NWS_API_BASE}/search_words"
    data = {'word': word, 'cookies': xianyu_cookies}
    result = await make_nws_request(url, data)
    if not result or "items" not in result:
        return "爬取失败，可能是闲鱼Cookies问题或者被限制了"
    if not result["items"]["data"]:
        return "爬取失败，可能是闲鱼Cookies问题或者被限制了"
    data = result['items']['data']
    list_word = list_word_format_alert(data)
    return [f"第{data + 1}级长尾词："+(",".join(list_word[data])) for data in list_word]


def run():
    mcp.run()


if __name__ == "__main__":
    run()
