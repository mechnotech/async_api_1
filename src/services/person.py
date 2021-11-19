import json
from functools import lru_cache
from typing import Optional, List

import elasticsearch.exceptions
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.config import FILM_CACHE_EXPIRE_IN_SECONDS
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from .utils import create_es_search_params


def clean_film_list(person_list: list) -> list:
    cleaned_data = []
    for person in person_list:
        cleaned_data.append(Person(**person['_source']))
    return cleaned_data


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_block(self, params: dict) -> Optional[List[Person]]:
        key = params.copy()
        key['key'] = 'persons_list'
        params = create_es_search_params(params)
        params.pop('sort')
        person_list = await self._person_list_from_cache(key)

        if not person_list:
            try:
                person_list = await self._get_person_list_from_es(params)
            except Exception:
                return None

        await self._put_person_list_raw_to_cache(persons=person_list, params=key)

        return clean_film_list(person_list)

    async def get_by_id(self, person_id: str) -> Optional[Person]:

        person = await self._person_from_cache(person_id)
        if not person:

            try:
                person = await self._get_person_from_elastic(person_id)
            except elasticsearch.exceptions.NotFoundError:
                return None

        await self._put_person_to_cache(person)

        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        doc = await self.elastic.get('persons', person_id)
        return Person(**doc['_source'])

    async def _get_person_list_from_es(self, params: dict) -> Optional[list]:
        doc = await self.elastic.search(index='persons', body=params)
        return doc['hits']['hits']

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        data = await self.redis.get(person_id)
        if not data:
            return None

        person = Person.parse_raw(data)
        return person

    async def _person_list_from_cache(self, params: dict) -> Optional[list]:
        data = await self.redis.get(str(params))
        if not data:
            return None
        return json.loads(data.decode('utf-8'))

    async def _put_person_to_cache(self, person: Person):
        await self.redis.set(person.id, person.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_person_list_raw_to_cache(self, persons: list, params: dict):
        await self.redis.set(key=str(params), value=json.dumps(persons), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
