from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Header

from core.config import Messages
from models.film import FilmShort, Film
from services.auth import get_user_role, is_user_privileged, privileged_only
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


@router.get('/{film_id}')
@privileged_only()
async def film_details(
        film_id: str,
        authorization: Optional[str] = Header(None),
        film_service: FilmService = Depends(get_film_service)) -> Film:
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
