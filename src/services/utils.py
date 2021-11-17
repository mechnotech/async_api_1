def create_es_search_params(params: dict) -> dict:
    page_sz = 20
    page_num = 0
    sort = 'imdb_rating'
    order = 'desc'
    genre_id = None
    query = None

    if params.get('sort'):
        if params['sort'][0] == '-':
            order = 'desc'
        else:
            order = 'asc'

    if params.get('page[size]'):
        page_sz = params.get('page[size]')
    if params.get('page[number]'):
        page_num = params.get('page[number]')
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
                            {"match": {"genre.uuid": genre_id}}

                        ]
                    }
                },
                "score_mode": "avg"
            }
        }

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
    if genre_id:
        template['query'] = filter_genres
    if query:
        template['query'] = search_query

    return template
