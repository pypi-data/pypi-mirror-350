#  ================================================
#   Made with heart by SCheck Team (© 2025)
#   https://scheck-blocklist.vercel.app
#
#  You MAY NOT:
#   - Use this code for commercial purposes.
#   - Remove credit or redistribute without license terms.
#
#   Respect the code. Respect the creator.
#  ================================================

import asyncio
import re
from typing import Optional, Pattern, List, Tuple

from .check import check_async
from .find import find_async
from .get import get_async
from .similar import similar_async

class Blocklist:
    @staticmethod
    def check(type_name: str, category: str, keyword: str) -> bool:
        if keyword.startswith(("https://", "http://")):
            keyword = keyword.split("/")[-1]
        return asyncio.run(check_async(type_name, category, keyword))
    
    @staticmethod
    def find(type_name: str, category: str, keyword: str) -> bool:
        if keyword.startswith(("https://", "http://")):
            keyword = keyword.split("/")[-1]
        return asyncio.run(find_async(type_name, category, keyword))

    @staticmethod
    def get(type_name: str, category: str, filename: Optional[str] = None, regex: Optional[Pattern] = None) -> List[str]:
        return asyncio.run(get_async(type_name, category, filename, regex))

    @staticmethod
    def similar(type_name: str, category: str, phrase: str, threshold: float = 0.6) -> List[Tuple[str, float]]:
        return asyncio.run(similar_async(type_name, category, phrase, threshold))
    
blocklist = Blocklist()