import json
from functools import lru_cache
from typing import Optional, List

import elasticsearch.exceptions
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from .utils import create_es_search_params

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


# def clean_film_list(films_list: list) -> list:
#     cleaned_data = []
#     for film in films_list:
#         cleaned_data.append(FilmToList(**film['_source']))
#     return cleaned_data


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # async def get_block(self, params: dict) -> Optional[List[Film]]:
    #     params = create_es_search_params(params)
    #
    #     films_list = await self._film_list_from_cache(params)
    #
    #     if not films_list:
    #         try:
    #             films_list = await self._get_film_list_from_es(params)
    #         except Exception:
    #             return None
    #
    #     await self._put_film_list_raw_to_cache(films=films_list, params=params)
    #
    #     return clean_film_list(films_list)


    async def get_by_id(self, genre_id: str) -> Optional[Genre]:

        genre = await self._film_from_cache(genre_id)
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

    async def _film_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(genre_id)
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    # async def _film_list_from_cache(self, params: dict) -> Optional[list]:
    #     data = await self.redis.get(str(params))
    #     if not data:
    #         return None
    #     return json.loads(data.decode())

    async def _put_genre_to_cache(self, genre: Genre):
        # Сохраняем данные о фильме, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(genre.id, genre.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    # async def _put_film_list_raw_to_cache(self, films: list, params: dict):
    #     await self.redis.set(key=str(params), value=json.dumps(films), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
