from http import HTTPStatus

from fastapi import HTTPException


def create_es_search_params(params: dict) -> dict:
    page_sz = 20
    page_num = 0
    sort = 'imdb_rating'
    order = 'desc'
    genre_id = None
    query = None

    if params.get('sort'):
        if not params['sort'][0] == '-':
            order = 'asc'

    if params.get('page[number]') and params.get('page[size]'):
        try:
            page_sz = int(params.get('page[size]'))
            page_num = int(params.get('page[number]'))
            if page_num > 1:
                page_num = page_num * page_sz
        except Exception:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='page[number], page[size] must be int')

    if params.get('filter[genre]'):
        genre_id = params.get('filter[genre]')
    if params.get('query'):
        query = params.get('query')

    search_query = {
        "query_string": {
            "fields": ["description", "title"],
            "query": f"{query}~"
        }
    }
    filter_genres = {
            "nested": {
                "path": "genre",
                "query": {
                    "bool": {
                        "must": [
                            {"match_phrase": {"genre.uuid": genre_id}}

                        ]
                    }
                },
                "score_mode": "avg"
            }
        }

    template = {
        "from": page_num,
        "size": page_sz,
    }
    temp_sort = [
        {
            sort: {
                "order": order
            }
        }
    ]
    if sort:
        template['sort'] = temp_sort
    if genre_id:
        template['query'] = filter_genres
    if query:
        template['query'] = search_query

    return template
