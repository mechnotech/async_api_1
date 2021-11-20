from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request

from core.config import Messages
from models.film import FilmShort, Film
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get("/")
@router.get("/search")
async def films_list(request: Request, film_service: FilmService = Depends(get_film_service)):
    film_list = await film_service.get_block(dict(request.query_params))
    if not film_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Messages.films_not_found)
    result = [FilmShort(id=x.id, title=x.title, imdb_rating=x.imdb_rating) for x in film_list]

    return result


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Messages.films_not_found)

    return Film(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=film.genre,
        actors=film.actors,
        writers=film.writers,
        directors=film.directors,
    )
