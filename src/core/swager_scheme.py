custom_scheme = {
    '/api/v1/film/': {
        'get': {
            'tags': ['Films entrypoint'],
            'summary': 'Films List',
            'operationId': 'films_list_api_v1_film__get',
            'parameters': [
                {
                    'required': False,
                    'schema': {'title': 'Page Size', 'type': 'integer', 'default': 20},
                    'name': 'page[size]',
                    'in': 'query',
                },
                {
                    'required': False,
                    'schema': {'title': 'Page Number', 'type': 'integer', 'default': 1},
                    'name': 'page[number]',
                    'in': 'query',
                },
                {
                    'required': False,
                    'schema': {
                        'title': 'Sort by field IMDB Rating (only)',
                        'type': 'string',
                        'default': '-imdb_rating',
                    },
                    'name': 'sort',
                    'in': 'query',
                },
                {
                    'required': False,
                    'schema': {'title': 'Filter by field', 'type': 'UUID', 'default': None},
                    'name': 'filter[genre]',
                    'in': 'query',
                },
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {}}}, },
                '422': {
                    'description': 'Validation Error',
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}},
                },
            },
        }
    },
    '/api/v1/film/search': {
        'get': {
            'tags': ['Films entrypoint'],
            'summary': 'Films List',
            'operationId': 'films_list_api_v1_film_search_get',
            'parameters': [
                {'required': True, 'schema': {'title': 'Query', 'type': 'string'}, 'name': 'query', 'in': 'query', },
                {
                    'required': False,
                    'schema': {'title': 'Page Size', 'type': 'integer', 'default': 20},
                    'name': 'page[size]',
                    'in': 'query',
                },
                {
                    'required': False,
                    'schema': {'title': 'Page Number', 'type': 'integer', 'default': 1},
                    'name': 'page[number]',
                    'in': 'query',
                },
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {}}}, },
                '422': {
                    'description': 'Validation Error',
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}},
                },
            },
        }
    },
    '/api/v1/film/{film_id}': {
        'get': {
            'tags': ['Films entrypoint'],
            'summary': 'Film Details',
            'operationId': 'film_details_api_v1_film__film_id__get',
            'parameters': [
                {'required': True, 'schema': {'title': 'Film Id', 'type': 'UUID'}, 'name': 'film_id', 'in': 'path', }
            ],
            'responses': {
                '200': {
                    'description': 'Successful Response',
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Film'}}},
                },
                '422': {
                    'description': 'Validation Error',
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}},
                },
            },
        }
    },
    '/api/v1/genre/': {
        'get': {
            'tags': ['Genres entrypoint'],
            'summary': 'Genres List',
            'operationId': 'genres_list_api_v1_genre__get',
            'parameters': [
                {
                    'required': False,
                    'schema': {'title': 'Page Size', 'type': 'integer', 'default': 20},
                    'name': 'page[size]',
                    'in': 'query',
                },
                {
                    'required': False,
                    'schema': {'title': 'Page Number', 'type': 'integer', 'default': 1},
                    'name': 'page[number]',
                    'in': 'query',
                },
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {}}}, }
            },
        }
    },
    '/api/v1/genre/{genre_id}': {
        'get': {
            'tags': ['Genres entrypoint'],
            'summary': 'Genre Details',
            'operationId': 'genre_details_api_v1_genre__genre_id__get',
            'parameters': [
                {'required': True, 'schema': {'title': 'Genre Id', 'type': 'UUID'}, 'name': 'genre_id', 'in': 'path', }
            ],
            'responses': {
                '200': {
                    'description': 'Successful Response',
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Genre'}}},
                },
                '422': {
                    'description': 'Validation Error',
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}},
                },
            },
        }
    },
    '/api/v1/person/': {
        'get': {
            'tags': ['Person entrypoint'],
            'summary': 'Persons List',
            'operationId': 'persons_list_api_v1_person__get',
            'parameters': [
                {
                    'required': False,
                    'schema': {'title': 'Page Size', 'type': 'integer', 'default': 20},
                    'name': 'page[size]',
                    'in': 'query',
                },
                {
                    'required': False,
                    'schema': {'title': 'Page Number', 'type': 'integer', 'default': 1},
                    'name': 'page[number]',
                    'in': 'query',
                },
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {}}}, }
            },
        }
    },
    '/api/v1/person/{person_id}/film/': {
        'get': {
            'tags': ['Person entrypoint'],
            'summary': 'Person Films',
            'operationId': 'person_films_api_v1_person__person_id__film__get',
            'parameters': [
                {
                    'required': False,
                    'schema': {'title': 'Page Size', 'type': 'integer', 'default': 20},
                    'name': 'page[size]',
                    'in': 'query',
                },
                {
                    'required': False,
                    'schema': {'title': 'Page Number', 'type': 'integer', 'default': 1},
                    'name': 'page[number]',
                    'in': 'query',
                },
                {
                    'required': True,
                    'schema': {'title': 'Person Id', 'type': 'UUID'},
                    'name': 'person_id',
                    'in': 'path',
                },
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {}}}, },
                '422': {
                    'description': 'Validation Error',
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}},
                },
            },
        }
    },
    '/api/v1/person/{person_id}/': {
        'get': {
            'tags': ['Person entrypoint'],
            'summary': 'Person Details',
            'operationId': 'person_details_api_v1_person__person_id___get',
            'parameters': [
                {'required': True, 'schema': {'title': 'Person Id', 'type': 'UUID'}, 'name': 'person_id',
                 'in': 'path', }
            ],
            'responses': {
                '200': {
                    'description': 'Successful Response',
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Person'}}},
                },
                '422': {
                    'description': 'Validation Error',
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}},
                },
            },
        }
    },
    '/api/v1/person/search': {
        'get': {
            'tags': ['Person entrypoint'],
            'summary': 'Search Persons',
            'operationId': 'search_persons_api_v1_person_search_get',
            'parameters': [
                {
                    'required': False,
                    'schema': {'title': 'Page Size', 'type': 'integer', 'default': 20},
                    'name': 'page[size]',
                    'in': 'query',
                },
                {
                    'required': False,
                    'schema': {'title': 'Page Number', 'type': 'integer', 'default': 1},
                    'name': 'page[number]',
                    'in': 'query',
                },
                {'required': True, 'schema': {'title': 'Query', 'type': 'string'}, 'name': 'query', 'in': 'query', },
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {}}}, },
                '422': {
                    'description': 'Validation Error',
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}},
                },
            },
        }
    },
}
