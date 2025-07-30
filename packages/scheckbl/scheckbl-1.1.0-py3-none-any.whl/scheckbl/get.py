import asyncio
import aiohttp
import re

BASE   = "SCheck-Blocklist"   
REPO   = "Datasets"           
BRANCH = "main"               


async def _get_json(session, url):
    async with session.get(url) as resp:
        if resp.status != 200:
            return None
        return await resp.json()

async def _download_text(session, download_url):
    async with session.get(download_url) as resp:
        resp.raise_for_status()
        return await resp.text()


async def _collect_texts(session, path, filename=None):
    api_url = (
        f"https://api.github.com/repos/{BASE}/{REPO}/contents/{path}?ref={BRANCH}"
    )
    data = await _get_json(session, api_url)
    if not data:
        return []

    tasks = []
    for entry in data:
        if entry["type"] == "dir":
            tasks.append(_collect_texts(session, entry["path"], filename))
        elif entry["type"] == "file" and entry["name"].endswith(".txt"):
            if filename is None or entry["name"] == filename:
                tasks.append(_download_text(session, entry["download_url"]))

    texts = []
    for coro in asyncio.as_completed(tasks):
        result = await coro
        if isinstance(result, list):
            texts.extend(result)
        else:
            texts.append(result)
    return texts


async def get_async(typ: str, cat: str, filename: str = None, regex: str = None) -> str:
    start_path = f"{typ}/{cat}"
    async with aiohttp.ClientSession() as session:
        texts = await _collect_texts(session, start_path, filename)
        combined = "\n".join(texts)
        if regex:
            pattern = re.compile(regex, re.IGNORECASE)
            filtered_lines = [line for line in combined.splitlines() if pattern.search(line)]
            return "\n".join(filtered_lines)
        return combined
