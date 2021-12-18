from typing import Optional

from .common import AdvancedJsonModel


class FilmShort(AdvancedJsonModel):
    title: str
    imdb_rating: Optional[float]


class Film(FilmShort):
    description: str
    genre: list
    actors: list
    writers: list
    directors: list
