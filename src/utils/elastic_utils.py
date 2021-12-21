import json
import os

from elasticsearch import Elasticsearch

from core.config import ELASTIC_HOST, ELASTIC_PORT
from utils.backoff_decorator import backoff

dir_path = os.path.dirname(os.path.realpath(__file__))

indexes_schemes = {
    'movies': 'movie_scheme_es.json',
    'genres': 'genre_scheme_es.json',
    'persons': 'person_scheme_es.json'
}
fixtures_files = {
    'genres': 'genres_fixtures.txt',
    'persons': 'persons_fixtures.txt',
    'movies': 'movies_fixtures.txt'
}


class ESConnector:

    def __init__(self):
        self.connection = Elasticsearch(host=ELASTIC_HOST, port=ELASTIC_PORT)
        self.connection.cluster.health(wait_for_status='yellow', request_timeout=1)

    def load(self, index: str, block: list):
        body = ''.join(block)
        self.connection.bulk(body=body, index=index, params={'filter_path': 'items.*.error'}, refresh=True)

    def is_index_exist(self, index: str):
        return self.connection.indices.exists(index=index)

    def create_index(self, index: str, file_name: str):
        with open(f'{dir_path}/../testdata/{file_name}', 'r') as f:
            self.connection.indices.create(index=index, body=json.load(f))
            return self.connection.indices.get(index=index)

    def __del__(self):
        self.connection.close()


def create_indexes():
    es_connect = ESConnector()
    for index, scheme in indexes_schemes.items():
        if not es_connect.is_index_exist(index=index):
            es_connect.create_index(index=index, file_name=scheme)


def apply_fixtures():
    es_connect = ESConnector()
    for index, fixtures in fixtures_files.items():
        with open(f'{dir_path}/../testdata/{fixtures}', 'r') as f:
            es_connect.load(index=index, block=f.readlines())


@backoff()
def apply_test_set():
    """
    К пустой тестовой ES применяем тестируемые индексы
    и набор данных. Набор тестовых данных сравнительно большой, поэтому
    желательна задержка, так-как ответ ES не означает, что изменения
    применены уже, а лишь то, что они будут приняты к применению.
    Либо применить refresh=True в bulk ES
    :return:
    """
    create_indexes()
    apply_fixtures()


if __name__ == '__main__':
    apply_test_set()
