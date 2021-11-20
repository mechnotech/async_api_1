import json
from collections import OrderedDict
from typing import Optional

import elasticsearch.exceptions
from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from core.config import FILM_CACHE_EXPIRE_IN_SECONDS
from .utils import create_es_search_params


class CommonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, short_obj, obj, key):
        """
        Объединяющий класс для всех сущностей Film, Genre, Person, отвечает за запросы в ES и
        кэширование в Redis
        :param redis:  Клиент Redis
        :param elastic: Клиент ElasticSearch
        :param short_obj: Сокращенная модель объекта запроса (Pydantic dataclass), например FilmShort
        :param obj: Развернутая модель объекта запроса (Pydantic dataclass)
        :param key: Индекс в ES, он же будет подмешиваться в ключ Redis для уникальности ключа

        """
        self.redis = redis
        self.elastic = elastic
        self.short_obj = short_obj
        self.obj = obj
        self.key = key

    async def get_block(self, params: dict, count_only=False) -> Optional[list]:
        key = params.copy()
        key['key'] = self.key
        key = OrderedDict(sorted(key.items()))
        params = create_es_search_params(params)

        block = await self._block_from_cache(key)
        if self.key != 'movies':
            params.pop('sort')
        if not block:
            try:
                block = await self._get_block_from_es(params)
            except Exception:
                return None

        await self._put_block_raw_to_cache(block=block, params=key)

        if count_only:
            return block['total']['value']
        return [self.short_obj(**x['_source']) for x in block['hits']]

    async def get_by_id(self, unit_id: str) -> Optional[object]:
        unit = await self._unit_from_cache(unit_id)
        if not unit:
            try:
                unit = await self._get_unit_from_elastic(unit_id)
            except elasticsearch.exceptions.NotFoundError:
                return None

        await self._put_unit_to_cache(unit)

        return unit

    async def _get_unit_from_elastic(self, unit_id: str) -> Optional[object]:
        doc = await self.elastic.get(self.key, unit_id)
        return self.obj(**doc['_source'])

    async def _get_block_from_es(self, params: dict) -> Optional[list]:
        doc = await self.elastic.search(index=self.key, body=params)
        return doc['hits']

    async def _unit_from_cache(self, unit_id: str) -> Optional[object]:
        data = await self.redis.get(self.key+unit_id)
        if not data:
            return None

        unit = self.obj.parse_raw(data)
        return unit

    async def _block_from_cache(self, params: dict) -> Optional[list]:
        data = await self.redis.get(str(params))
        if not data:
            return None
        return json.loads(data.decode('utf-8'))

    async def _put_unit_to_cache(self, unit):
        exists = await self.redis.exists(self.key + unit.id)
        if exists:
            await self.redis.expire(self.key + unit.id, FILM_CACHE_EXPIRE_IN_SECONDS)
        await self.redis.set(self.key + unit.id, unit.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_block_raw_to_cache(self, block: list, params: dict):
        exists = await self.redis.exists(str(params))
        if exists:
            await self.redis.expire(str(params), FILM_CACHE_EXPIRE_IN_SECONDS)
        await self.redis.set(key=str(params), value=json.dumps(block), expire=FILM_CACHE_EXPIRE_IN_SECONDS)
