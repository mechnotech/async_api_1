from http import HTTPStatus

from fastapi import HTTPException


def create_es_search_params(params: dict) -> dict:
    page_sz = 20
    page_num = 0
    sort = 'imdb_rating'
    order = 'desc'
    filter_id = None
    filter_path = None
    query = None
    query_fields = ['title,', 'description']

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
        filter_id = params.get('filter[genre]')
        filter_path = 'genre'
    if params.get('filter[person]'):
        filter_id = params.get('filter[person]')
    if params.get('filter[path]'):
        filter_path = params.get('filter[path]')
    if params.get('query'):
        query = params.get('query')
    if params.get('fields'):
        if isinstance(params.get('fields'), list):
            query_fields = params.get('fields')
        else:
            query_fields = [params.get('fields')]

    search_query = {
        "query_string": {
            "fields": query_fields,
            "query": f"{query}~"
        }
    }
    temp_filter = {
        "nested": {
            "path": filter_path,
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {f"{filter_path}.uuid": filter_id}}

                    ]
                }
            }
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
    if filter_id:
        template['query'] = temp_filter
    if query:
        template['query'] = search_query

    return template
