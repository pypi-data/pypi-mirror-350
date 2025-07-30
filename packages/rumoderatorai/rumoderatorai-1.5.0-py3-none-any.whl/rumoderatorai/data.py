from typing import Final

import platform

import aiohttp


__version__ = "1.5.0"

API_VERSION: Final[str] = "v3"

HEADERS: Final[dict[str, str]] = {
    "User-Agent": f"RuModeratorAI Python Library/{__version__} (Python {platform.python_version()}) via aiohttp/{aiohttp.__version__}"
}
