import asyncio
import aiohttp
import re

BASE = "SCheck-Blocklist"
REPO = "Datasets"
BRANCH = "main"

async def get_json(s, url):
    async with s.get(url) as r:
        if r.status != 200:
            return None
        return await r.json()

async def check_file(s, url, kw, path):
    async with s.get(url) as r:
        if r.status != 200:
            return False
        text = await r.text()
        pattern = re.compile(rf'\b{re.escape(kw)}\b', re.IGNORECASE)
        if pattern.search(text):
            return True
    return False

async def search(s, path, kw):
    url = f"https://api.github.com/repos/{BASE}/{REPO}/contents/{path}?ref={BRANCH}"
    data = await get_json(s, url)
    if not data:
        return False
    tasks = []
    for f in data:
        if f["type"] == "dir":
            tasks.append(search(s, f["path"], kw))
        elif f["type"] == "file" and f["name"].endswith(".txt"):
            tasks.append(check_file(s, f["download_url"], kw, f["path"]))
    for t in asyncio.as_completed(tasks):
        if await t:
            return True
    return False

async def check_async(typ, cat, keyword):
    path = f"{typ}/{cat}"
    async with aiohttp.ClientSession() as s:
        return await search(s, path, keyword)
