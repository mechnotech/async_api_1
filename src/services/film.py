from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmShort
from .base import BaseCacheEngine, BaseSearchEngine
from .common import CommonService


class FilmService(CommonService):
    pass


@lru_cache()
def get_film_service(
        redis: BaseCacheEngine = Depends(get_redis),
        elastic: BaseSearchEngine = Depends(get_elastic),
) -> FilmService:
    return FilmService(
        cache_engine=redis,
        search_engine=elastic,
        short_obj=FilmShort,
        obj=Film,
        key='movies'
    )
