import datetime
from typing import Optional

import orjson

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class PersonShort(BaseModel):
    id: str
    full_name: str
    birthday: Optional[datetime.date]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(PersonShort):
    role: Optional[dict]