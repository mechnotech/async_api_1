from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()



# @router.get("/")
# async def films_list(sort: str, request: Request, film_service: FilmService = Depends(get_film_service)):
#     film_list = await film_service.get_block(dict(request.query_params))
#     if not film_list:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')
#     result = [FilmToList(id=x.id, title=x.title, imdb_rating=x.imdb_rating) for x in film_list]
#     return result
#
#
# @router.get("/search")
# async def search_films(request: Request, film_service: FilmService = Depends(get_film_service)):
#     film_list = await film_service.get_block(dict(request.query_params))
#     if not film_list:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')
#     result = [FilmToList(id=x.id, title=x.title, imdb_rating=x.imdb_rating) for x in film_list]
#     return result


@router.get('/{genre_id}', response_model=Genre)
async def film_details(genre_id: str, film_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await film_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return Genre(
        id=genre.id,
        name=genre.name,
        description=genre.description,
        )
