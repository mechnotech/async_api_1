from typing import Optional

from .common import AdvancedJsonModel


class GenreShort(AdvancedJsonModel):
    name: str
    description: Optional[str]


class Genre(GenreShort):
    score: Optional[int]
