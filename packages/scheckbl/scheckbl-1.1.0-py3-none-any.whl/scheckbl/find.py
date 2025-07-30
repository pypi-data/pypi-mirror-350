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

async def check_file(s, url, pattern):
    async with s.get(url) as r:
        if r.status != 200:
            return False
        text = await r.text()
        return bool(pattern.search(text))

async def search(s, path, pattern):
    url = f"https://api.github.com/repos/{BASE}/{REPO}/contents/{path}?ref={BRANCH}"
    data = await get_json(s, url)
    if not data:
        return False

    tasks = []
    for f in data:
        if f["type"] == "dir":
            tasks.append(search(s, f["path"], pattern))
        elif f["type"] == "file" and f["name"].endswith(".txt"):
            tasks.append(check_file(s, f["download_url"], pattern))

    for t in asyncio.as_completed(tasks):
        if await t:
            return True
    return False


def build_pattern(phrase: str) -> re.Pattern:
    tokens = re.findall(r'\w+', phrase.lower())
    escaped = [re.escape(tok) for tok in tokens if tok] 
    regex = r'\b(?:' + '|'.join(escaped) + r')\b'
    return re.compile(regex, re.IGNORECASE)

async def find_async(typ: str, cat: str, phrase: str) -> bool:
    pattern = build_pattern(phrase)
    path = f"{typ}/{cat}"
    async with aiohttp.ClientSession() as s:
        return await search(s, path, pattern)
