from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from models.genre import Genre, GenreShort
from services.film import FilmService, get_film_service
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get("/")
async def genres_list(
        request: Request,
        genre_service: GenreService = Depends(get_genre_service),

):
    genre_list = await genre_service.get_block(dict(request.query_params))
    if not genre_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    result = [GenreShort(id=x.id, name=x.name, description=x.description) for x in genre_list]
    return result


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service),
        film_service: FilmService = Depends(get_film_service),
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    query_params = dict()
    query_params['filter[genre]'] = genre.id
    score = await film_service.get_block(query_params, count_only=True)

    return Genre(
        id=genre.id,
        name=genre.name,
        description=genre.description,
        score=score,
    )
