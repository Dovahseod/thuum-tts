import json
import os

import aiofiles

ROOT_DIR = os.path.join(os.path.dirname(__file__), '../../')


class JsonAIO:
    def __init__(self, filename: str, default_value: dict | list = {}) -> None:
        self.filepath = os.path.join(ROOT_DIR, "data", filename)
        self.default_value = default_value
        self.cache: dict | list | None = None

    async def read(self) -> dict | list:
        try:
            async with aiofiles.open(self.filepath) as f:
                contents = await f.read()
                data: dict | list = json.loads(contents)
                return data
        except FileNotFoundError:
            return self.default_value

    async def read_cache(self) -> dict | list:
        if self.cache is None:
            data = await self.read()
            self.cache = data.copy()
        return self.cache

    async def write(self, data: dict | list) -> None:
        async with aiofiles.open(self.filepath, 'w') as f:
            if self.cache is not None:
                self.cache = data.copy()
            await f.write(json.dumps(data))
