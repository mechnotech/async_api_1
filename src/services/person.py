from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person, PersonShort
from .base import BaseCacheEngine, BaseSearchEngine
from .common import CommonService


class PersonService(CommonService):
    pass


@lru_cache()
def get_person_service(
    redis: BaseCacheEngine = Depends(get_redis), elastic: BaseSearchEngine = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache_engine=redis, search_engine=elastic, short_obj=PersonShort, obj=Person, key='persons')
