import orjson

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FilmShort(BaseModel):
    id: str
    title: str
    imdb_rating: float

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(FilmShort):
    description: str
    genre: list
    actors: list
    writers: list
    directors: list
