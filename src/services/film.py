import json
from collections import OrderedDict
from functools import lru_cache
from typing import Optional, List

import elasticsearch.exceptions
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.config import FILM_CACHE_EXPIRE_IN_SECONDS
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmShort
from .utils import create_es_search_params


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_block(self, params: dict, count_only=False) -> Optional[List[FilmShort]]:
        key = params.copy()
        key['key'] = 'films_list'
        key = OrderedDict(sorted(key.items()))
        params = create_es_search_params(params)

        films = await self._film_list_from_cache(key)

        if not films:
            try:
                films = await self._get_film_list_from_es(params)
            except Exception:
                return None

        await self._put_film_list_raw_to_cache(films=films, params=key)

        if count_only:
            return films['total']['value']
        return [FilmShort(**x['_source']) for x in films['hits']]

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            try:
                film = await self._get_film_from_elastic(film_id)
            except elasticsearch.exceptions.NotFoundError:
                return None

        await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        doc = await self.elastic.get('movies', film_id)
        return Film(**doc['_source'])

    async def _get_film_list_from_es(self, params: dict) -> Optional[list]:
        doc = await self.elastic.search(index='movies', body=params)
        return doc['hits']

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _film_list_from_cache(self, params: dict) -> Optional[list]:
        data = await self.redis.get(str(params))
        if not data:
            return None
        return json.loads(data.decode('utf-8'))

    async def _put_film_to_cache(self, film: Film):
        if await self.redis.exists(film.id):
            await self.redis.expire(film, FILM_CACHE_EXPIRE_IN_SECONDS)
        await self.redis.set(film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_film_list_raw_to_cache(self, films: list, params: dict):
        if await self.redis.exists(str(params)):
            await self.redis.expire(str(params), FILM_CACHE_EXPIRE_IN_SECONDS)
        await self.redis.set(key=str(params), value=json.dumps(films), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
