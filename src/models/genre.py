from typing import Optional

import orjson

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class GenreShort(BaseModel):
    id: str
    name: str
    description: Optional[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Genre(GenreShort):
    score: Optional[int]
