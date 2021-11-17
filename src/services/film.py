import json
from functools import lru_cache
from typing import Optional, List

import elasticsearch.exceptions
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmToList

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


def create_es_search_params(params: dict) -> dict:
    page_sz = 20
    page_num = 0
    sort = 'imdb_rating'

    if params['sort'][0] == '-':
        order = 'desc'
    else:
        order = 'asc'

    if params.get('page[size]'):
        page_sz = params.get('page[size]')
    if params.get('page[number]'):
        page_num = params.get('page[number]')

    template = {
        "from": page_num,
        "size": page_sz,
        "sort": [
            {
                sort: {
                    "order": order
                }
            }
        ]
    }

    return template


def clean_film_list(films_list: list) -> list:
    cleaned_data = []
    for film in films_list:
        cleaned_data.append(FilmToList(**film['_source']))
    return cleaned_data


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_block(self, params: dict) -> Optional[List[Film]]:
        params = create_es_search_params(params)

        films_list = await self._film_list_from_cache(params)

        if not films_list:
            try:
                films_list = await self._get_film_list_from_es(params)
            except Exception:
                return None

        await self._put_film_list_raw_to_cache(films=films_list, params=params)

        return clean_film_list(films_list)

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film = await self._film_from_cache(film_id)
        if not film:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            try:
                film = await self._get_film_from_elastic(film_id)
            except elasticsearch.exceptions.NotFoundError:
                return None

        # Сохраняем/обновляем фильм в кешe
        await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        doc = await self.elastic.get('movies', film_id)
        return Film(**doc['_source'])

    async def _get_film_list_from_es(self, params: dict) -> Optional[list]:
        doc = await self.elastic.search(index='movies', body=params)
        return doc['hits']['hits']

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(film_id)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        film = Film.parse_raw(data)
        return film

    async def _film_list_from_cache(self, params: dict) -> Optional[list]:
        data = await self.redis.get(str(params))
        if not data:
            return None
        return json.loads(data.decode())

    async def _put_film_to_cache(self, film: Film):
        # Сохраняем данные о фильме, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_film_list_raw_to_cache(self, films: list, params: dict):
        await self.redis.set(key=str(params), value=json.dumps(films), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
