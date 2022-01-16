from functools import wraps
from http import HTTPStatus

import aiohttp
from fastapi import HTTPException

from core.config import PRIVILEGED_USERS_ROLES, AUTH_API, AUTH_PORT, Messages


def is_user_privileged(roles):
    return set(roles) & set(PRIVILEGED_USERS_ROLES)


async def get_user_role(auth_token) -> list:
    if not auth_token:
        return ['Anonymous', ]
    headers = {'Authorization': auth_token, "Accept": 'application/json'}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'http://{AUTH_API}:{AUTH_PORT}/api/v1/users/me/') as r:
            if r.status != 200:
                return ['Anonymous', ]
            json_body = await r.json()
    msg = json_body.get('msg')
    if msg:
        roles = msg.get('role')
    else:
        return ['Anonymous', ]
    if not roles:
        return ['Anonymous', ]
    return roles


def privileged_only():
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            authorization = kwargs.get('authorization')
            user_role = await get_user_role(authorization)
            if not is_user_privileged(user_role):
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=Messages.paid_content)
            result = await f(*args, **kwargs)
            return result

        return wrapper

    return decorator
