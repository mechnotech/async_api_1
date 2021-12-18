import aiohttp

from core.config import PRIVILEGED_USERS_ROLES, AUTH_API, AUTH_PORT


def is_user_privileged(roles):
    return set(roles) & set(PRIVILEGED_USERS_ROLES)


async def get_user_role(request) -> list:
    auth_token = request.headers.get('authorization')
    if not auth_token:
        return ['Anonymous', ]
    headers = {'Authorization': auth_token, "Accept": 'application/json'}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'http://{AUTH_API}:{AUTH_PORT}/api/v1/users/me/') as r:
            json_body = await r.json()
    msg = json_body.get('msg')
    if msg:
        roles = msg.get('role')
    else:
        return ['Anonymous', ]
    if not roles:
        return ['Anonymous', ]
    return roles
