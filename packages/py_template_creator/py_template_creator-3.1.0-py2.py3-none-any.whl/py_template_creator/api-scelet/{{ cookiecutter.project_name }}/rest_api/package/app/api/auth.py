from fastapi import APIRouter, Response, Request, Depends
from package.app.schemas import (
    BaseResponseSchema,
    UserCreateRequestSchema,
    UserResponseSchema,
    UserLoginResponseSchema,
    UserLoginRequestSchema,
    UserRefreshTokenSchema,
)
from package.app.utilities import (
    CustomHTTPException,
    RateLimiter,
    DBSessionDep,
)
from package.app.auth import AuthHandler, JWTBearer
import logging
from package.app import managers
from package.app.cache import RefreshTokenCache

logger = logging.getLogger(__name__)

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post(
    "/login",
)
async def login(
    db_session: DBSessionDep,
    response: Response,
    request: Request,
    request_user: UserLoginRequestSchema,
) -> UserLoginResponseSchema | BaseResponseSchema:
    """
    In this demo version, we dont check if user phone and email
    or whatever is verified, since we would do that with some kind
    of external service, which this template is not about.
    So in a real project, you would deny login(or not?)
    if user does not have a verified phone / mail address.
    """
    user_id = await managers.UserManager(
        db_session
    ).check_login_credentials_and_get_id(
        email=request_user.email, password=request_user.password
    )
    if user_id:
        tokens = await AuthHandler.make_auth_tokens(user_id)
        return tokens
    response.status_code = 403
    return {"message": "Invalid credentials"}


@auth_router.post(
    "/register",
    status_code=201,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def register(
    db_session: DBSessionDep,
    response: Response,
    request: Request,
    user: UserCreateRequestSchema,
) -> UserResponseSchema | BaseResponseSchema:
    user_manager = managers.UserManager(db_session)
    phone_exists = await user_manager.check_if_user_phone_exists(
        phone=user.phone
    )
    if phone_exists:
        raise CustomHTTPException(
            message="Phone already exists",
            status_code=409,
        )
    email_exists = await user_manager.check_if_user_email_exists(user.email)
    if email_exists:
        raise CustomHTTPException(
            message="Email already exists",
            status_code=409,
        )
    user = await user_manager.create(user.model_dump())
    return user


@auth_router.post(
    "/refresh",
)
async def refresh(
    db_session: DBSessionDep,
    response: Response,
    request: Request,
    body: UserRefreshTokenSchema,
) -> UserLoginResponseSchema | BaseResponseSchema:
    token = AuthHandler.decodeJWT(body.refresh_token, "refresh")
    if token:
        refresh_token_cache = await RefreshTokenCache().retrieve(
            token["user_id"], body.refresh_token
        )
        if refresh_token_cache:
            await AuthHandler.delete_refresh_token(
                token["user_id"], body.refresh_token
            )
            user = await managers.UserManager(db_session).get_single(
                filters={"id": token["user_id"]}
            )
            if user:
                tokens = await AuthHandler.make_auth_tokens(token["user_id"])
                return tokens
    response.status_code = 401
    return {"message": "Invalid refresh token"}


@auth_router.post("/logout", dependencies=[Depends(JWTBearer())])
async def logout(
    response: Response, request: Request, body: UserRefreshTokenSchema
) -> BaseResponseSchema:
    user_id = request.credentials["user_id"]
    await AuthHandler.delete_refresh_token(user_id, body.refresh_token)
    response.status_code = 200
    return {"message": "Logged out"}
