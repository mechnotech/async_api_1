from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get("/")
async def films_list(request: Request, genre_service:  GenreService = Depends(get_genre_service)):
    genre_list = await genre_service.get_block(dict(request.query_params))
    if not genre_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    result = [Genre(id=x.id, name=x.name, description=x.description) for x in genre_list]
    return result


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
