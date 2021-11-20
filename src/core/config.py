import os
from dataclasses import dataclass
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)
FILM_CACHE_EXPIRE_IN_SECONDS = os.getenv('REDIS_CASH_SECONDS', 360)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'elasticsearch')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class Messages:
    bad_page_params = 'page[number], page[size] must be int'
    films_not_found = 'Films not found'
    genres_not_found = 'Genres not found'
    persons_not_found = 'Persons not found'
