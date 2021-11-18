from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from models.person import Person
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get("/")
async def films_list(request: Request, person_service:  PersonService = Depends(get_person_service)):
    person_list = await person_service.get_block(dict(request.query_params))
    if not person_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')
    result = [Person(id=x.id, full_name=x.full_name, birthday=x.birthday) for x in person_list]
    return result


@router.get('/{person_id}', response_model=Person)
async def film_details(person_id: str, film_service: PersonService = Depends(get_person_service)) -> Person:
    person = await film_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return Person(
        id=person.id,
        full_name=person.full_name,
        birthday=person.birthday,
    )
