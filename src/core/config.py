import os
from dataclasses import dataclass
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)
FILM_CACHE_EXPIRE_IN_SECONDS = int(os.getenv('REDIS_CASH_SECONDS', 360))

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))
AUTH_API = os.getenv('AUTH_API', '127.0.0.1')
AUTH_PORT = int(os.getenv('AUTH_PORT', 8500))
ROLES_GET_ENDPOINT = os.getenv('ROLES_ENDPOINT', 'api/v1/users/me')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Доступы к контенту

ADMIN_ROLES = ['admin', 'moderator']
PRIVILEGED_USERS_ROLES = ['subscriber', 'bonus', 'trial']
PRIVILEGED_USERS_ROLES += ADMIN_ROLES


@dataclass
class Messages:
    paid_content = 'Контент только для подписчиков'
    bad_page_params = 'page[number], page[size] must be int'
    films_not_found = 'Films not found'
    genres_not_found = 'Genres not found'
    persons_not_found = 'Persons not found'
