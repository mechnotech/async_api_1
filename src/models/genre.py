from typing import Optional

from .common import AdvancedJsonModel


class GenreShort(AdvancedJsonModel):
    id: str
    name: str
    description: Optional[str]


class Genre(GenreShort):
    score: Optional[int]
