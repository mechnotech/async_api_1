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
from models.genre import Genre
from .utils import create_es_search_params


def clean_film_list(genre_list: list) -> list:
    cleaned_data = []
    for genre in genre_list:
        cleaned_data.append(Genre(**genre['_source']))
    return cleaned_data


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_block(self, params: dict) -> Optional[List[Genre]]:
        key = params.copy()
        key['key'] = 'genres_list'
        params = create_es_search_params(params)
        params.pop('sort')
        genre_list = await self._genre_list_from_cache(key)

        if not genre_list:
            try:
                genre_list = await self._get_genre_list_from_es(params)
            except Exception:
                return None

        await self._put_genre_list_raw_to_cache(genres=genre_list, params=key)

        return clean_film_list(genre_list)

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:

        genre = await self._genre_from_cache(genre_id)
        if not genre:

            try:
                genre = await self._get_genre_from_elastic(genre_id)
            except elasticsearch.exceptions.NotFoundError:
                return None

        await self._put_genre_to_cache(genre)

        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        doc = await self.elastic.get('genres', genre_id)
        return Genre(**doc['_source'])

    async def _get_genre_list_from_es(self, params: dict) -> Optional[list]:
        doc = await self.elastic.search(index='genres', body=params)
        return doc['hits']['hits']

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(genre_id)
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    async def _genre_list_from_cache(self, params: dict) -> Optional[list]:
        data = await self.redis.get(str(params))
        if not data:
            return None
        return json.loads(data.decode('utf-8'))

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(genre.id, genre.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_genre_list_raw_to_cache(self, genres: list, params: dict):
        await self.redis.set(key=str(params), value=json.dumps(genres), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
