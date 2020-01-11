import asyncio
import requests

from .validator import api_validator


async def request(url):
    print(url)
    res = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
    print(url, res.status_code)
    api_validator('request', res)


def run():
    urls = ['http://www.baidu.com', 'http://www.bilibili.com']
    tasks = [request(url) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
