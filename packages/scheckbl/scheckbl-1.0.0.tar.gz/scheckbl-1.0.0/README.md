# SCheck Blocklist

**Python package enabling seamless integration with the SCheck Blocklist datasets**
> Actually Version: `1.0.0`
> 
> Our Websites: [scheck-blocklist.vercel.app](https://scheck-blocklist.vercel.app)

---

## Content
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
  - [blocklist.check](#blocklistcheck)
  - [blocklist.find](#blocklistfind)
  - [blocklist.get](#blocklistget)
  - [blocklist.similar](#blocklistsimilar)


---

## Installation

To download a library from PyPI via pip just use the command:

```bash
pip install scheckbl
```

---

## Quick Start

Below is sample code showing the syntax:

```python
from scheckbl import blocklist

c = blocklist.check("phrases", "vulgarisms", "f*ck")        # output: True
f = blocklist.find("phrases", "vulgarisms", "I f*ck you")    # output: True
g = blocklist.get("urls", "ads")                              # output: list
s = blocklist.similar("phrases", "vulgarisms", "f*uck", 0.3) # output: json
```

---

## API Reference

### `blocklist.check`

Checks whether a given keyword is present in the specified blocklist.

* `type_name`: category group, e.g., "phrases" or "urls"
* `category`: sublist name, e.g., "vulgarisms", "ads"
* `keyword`: the word or phrase to check
* **Returns**: `True` if keyword is found on the blocklist; otherwise, `False`

📌 **Note**: If `keyword` is a URL, the last segment (after the last `/`) is automatically extracted before checking.

---

### `blocklist.find`

Checks whether any part of the keyword string contains entries from the blocklist.

* `type_name`: same as above
* `category`: same as above
* `keyword`: full sentence or input string to search through
* **Returns**: `True` if any blocklisted entry is found; otherwise, `False`

📌 **Note**: Just like `check()`, URLs will be trimmed to their final segment.

---

### `blocklist.get`

Retrieves the full blocklist for the given category.

* `type_name`: e.g. "phrases"
* `category`: e.g. "ads"
* `filename` (optional): specific file to load
* `regex` (optional): regex pattern to filter results
* **Returns**: a list of strings representing the full blocklist, each entry as a separate line

---

### `blocklist.similar`

Finds entries in the blocklist that are similar to the input phrase.

* `type_name`: e.g., "phrases"
* `category`: e.g., "vulgarisms"
* `phrase`: the string to compare
* `threshold`: similarity threshold from 0.0 to 1.0 (default: 0.6)
* **Returns**: list of tuples `(entry: str, similarity: float)` representing blocklist entries with similarity scores



Created with ❤️ by SCheck-Team
