from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from core.config import Messages
from models.film import FilmShort
from models.person import Person, PersonShort
from services.film import FilmService, get_film_service
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/')
async def persons_list(request: Request, person_service: PersonService = Depends(get_person_service)):
    person_list = await person_service.get_block(dict(request.query_params))
    if not person_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Messages.persons_not_found)
    result = [PersonShort(id=x.id, full_name=x.full_name, birthday=x.birthday) for x in person_list]
    return result


@router.get('/{person_id}/film/')
async def person_films(
    request: Request,
    person_id: str,
    film_service: FilmService = Depends(get_film_service),
    person_service: PersonService = Depends(get_person_service),
):
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Messages.persons_not_found)

    query_params = dict(request.query_params)
    query_params['filter[person]'] = person.id
    roles = ['actors', 'writers', 'directors']
    film_list = []
    for role in roles:
        query_params['filter[path]'] = role
        films = await film_service.get_block(query_params)
        if films:
            film_list += films
    if not film_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Messages.persons_not_found)
    result = [FilmShort(id=x.id, title=x.title, imdb_rating=x.imdb_rating) for x in film_list]
    return result


@router.get('/{person_id}/', response_model=Person)
async def person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service),
) -> Person:
    person_role = {'writer': [], 'actor': [], 'director': []}
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Messages.persons_not_found)

    query_params = dict()
    for role in person_role.keys():
        query_params['filter[person]'] = person.id
        query_params['filter[path]'] = f'{role}s'
        film_list = await film_service.get_block(query_params)
        if film_list:
            person_role[role] = [x.id for x in film_list]

    return Person(id=person.id, full_name=person.full_name, birthday=person.birthday, role=person_role)


@router.get('/search')
async def search_persons(request: Request, person_service: PersonService = Depends(get_person_service)):
    query_params = dict(request.query_params)
    query_params['fields'] = 'full_name'
    person_list = await person_service.get_block(query_params)

    if not person_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=Messages.persons_not_found)
    result = [PersonShort(id=x.id, full_name=x.full_name, birthday=x.birthday) for x in person_list]
    return result
