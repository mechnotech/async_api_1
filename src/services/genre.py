from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre, GenreShort
from .base import BaseCacheEngine, BaseSearchEngine
from .common import CommonService


class GenreService(CommonService):
    pass


@lru_cache()
def get_genre_service(
    redis: BaseCacheEngine = Depends(get_redis), elastic: BaseSearchEngine = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache_engine=redis, search_engine=elastic, short_obj=GenreShort, obj=Genre, key='genres')
