from fastapi import APIRouter, Response, Request, Depends
from package.app.schemas import (
    BaseResponseSchema,
    UserResponseSchema,
    Page,
)
from mrkutil.pagination import pagination_params
from package.app.utilities import (
    RateLimiter,
    DBSessionDep,
)
from package.app.auth import JWTBearer
import logging
from package.app import managers

logger = logging.getLogger(__name__)

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# Example pagination authenticated API for getting all users
@user_router.get(
    "/all",
    status_code=200,
    dependencies=[
        Depends(RateLimiter(times=5, seconds=60)),
        Depends(JWTBearer()),
    ],
)
async def get_all_users(
    db_session: DBSessionDep,
    response: Response,
    request: Request,
    params: dict = Depends(pagination_params),
) -> Page[UserResponseSchema] | BaseResponseSchema:
    user_manager = managers.UserManager(db_session)
    users = await user_manager.get_paginated(filters={}, **params)
    return users
