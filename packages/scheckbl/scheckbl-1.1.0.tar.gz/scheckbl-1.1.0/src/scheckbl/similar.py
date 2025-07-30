import asyncio
import aiohttp
import re
import difflib

BASE = "SCheck-Blocklist"
REPO = "Datasets"
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

async def _collect_texts(session, path):
    api_url = f"https://api.github.com/repos/{BASE}/{REPO}/contents/{path}?ref={BRANCH}"
    data = await _get_json(session, api_url)
    if not data:
        return []
    tasks = []
    for e in data:
        if e["type"] == "dir":
            tasks.append(_collect_texts(session, e["path"]))
        elif e["type"] == "file" and e["name"].endswith(".txt"):
            tasks.append(_download_text(session, e["download_url"]))
    texts = []
    for c in asyncio.as_completed(tasks):
        r = await c
        if isinstance(r, list):
            texts.extend(r)
        else:
            texts.append(r)
    return texts

_leet = str.maketrans({
    '4': 'a', '@': 'a',
    '3': 'e',
    '0': 'o',
    '6': 'g',
    '1': 'l', '|': 'l', '!': 'i',
    '5': 's', '$': 's',
    '7': 't', '+': 't'
})

def _norm(s: str) -> str:
    return s.lower().translate(_leet)

async def get_async(typ: str, cat: str, regex: str = None) -> str:
    start_path = f"{typ}/{cat}"
    async with aiohttp.ClientSession() as session:
        texts = await _collect_texts(session, start_path)
        combined = "\n".join(texts)
        if regex:
            patt = re.compile(regex, re.IGNORECASE)
            return "\n".join(l for l in combined.splitlines() if patt.search(l))
        return combined

async def similar_async(typ: str, cat: str, word: str, threshold: float = 0.6) -> dict[str, float]:
    raw = await get_async(typ, cat)
    target = _norm(word)
    seen = set()
    results = {}
    for line in raw.splitlines():
        clean = line.strip()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        ratio = difflib.SequenceMatcher(None, _norm(clean), target).ratio()
        if ratio >= threshold:
            results[clean] = round(ratio, 3)
    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


