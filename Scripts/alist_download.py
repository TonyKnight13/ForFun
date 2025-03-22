'''
Author: Taony
Date: 2024-03-30 20:52:52
LastEditors: Taony
LastEditTime: 2024-03-30 20:55:04
FilePath: \ForFun\Scripts\alist_download.py
'''
import asyncio
import time
import urllib.parse
from xml.etree import ElementTree as ET

import aiohttp

BASE_URL = "http://38.46.31.239:5244"
USER = "avalon-plan"
PASSWORD = "13763143589"


async def fetch(
    session: aiohttp.ClientSession, queue: asyncio.Queue, path: str
) -> None:
    headers = {
        "Cookie": "你的浏览器 Cookie，包含cf_clearance=xxxx",
        "User-Agent": "你的浏览器 User-Agent",
        "Depth": "1",
    }
    url = BASE_URL + path
    async with session.request("PROPFIND", url, headers=headers) as response:
        if response.status in (207, 301):
            tree = ET.fromstring(await response.text())
            for item in tree.findall(".//{DAV:}href"):
                file_path = urllib.parse.unquote(item.text or "")
                if file_path == path:
                    continue

                await queue.put(file_path)
        else:
            print(f"{url} 请求失败: {response.status}")


async def worker(
    session: aiohttp.ClientSession, queue: asyncio.Queue[str], files: list[str]
) -> None:
    while True:
        path = await queue.get()
        if path.endswith("/"):
            print(path)
            await fetch(session, queue, path)
        else:
            files.append(BASE_URL + path.replace("/dav", "", 1))

        queue.task_done()


async def main() -> None:
    start = time.monotonic()
    files: list[str] = []
    # dirs = ["漫画盘1", "漫画盘2"]
    dirs = [""]

    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(USER, PASSWORD)) as session:
        queue = asyncio.Queue()
        for dir in dirs:
            if dir and not dir.endswith("/"):
                dir += "/"
            queue.put_nowait(f"/dav/{dir}")

        tasks = [asyncio.create_task(worker(session, queue, files)) for _ in range(20)]
        await queue.join()

        for task in tasks:
            task.cancel()

        with open("manga.txt", "w", encoding="utf8") as f:
            f.write("\n".join(sorted(files)))

    print(f"完成。文件：{len(files)}，耗时：{time.monotonic() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())