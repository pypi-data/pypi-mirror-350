import time as t
import logging
import jwt
from package.app import settings
from package.app.cache import RefreshTokenCache

logger = logging.getLogger(__name__)


class AuthHandler:
    JWT_ALGORITHM = settings.JWT_ALGORITHM
    JWT_SECRET = settings.JWT_SECRET
    REFRESH_JWT_SECRET = settings.REFRESH_JWT_SECRET
    TOKEN_TYPES = {
        "access": JWT_SECRET,
        "refresh": REFRESH_JWT_SECRET,
    }
    JWT_EXPIRE = settings.JWT_EXPIRE
    REFRESH_JWT_EXPIRE = settings.REFRESH_JWT_EXPIRE
    TOKEN_EXPIRES = {
        "access": JWT_EXPIRE,
        "refresh": REFRESH_JWT_EXPIRE,
    }

    @classmethod
    async def signJWT(cls, user_id: str) -> dict:
        return {
            "access_token": await cls.sign_access_token(
                user_id,
            ),
            "refresh_token": await cls.sign_refresh_token(user_id),
        }

    @classmethod
    def decodeJWT(cls, token: str, token_type: str) -> dict:
        try:
            token = jwt.decode(
                token,
                cls.TOKEN_TYPES.get(token_type),
                algorithms=[cls.JWT_ALGORITHM],
            )
            if token["exp"] >= t.time():
                return token
        except Exception as e:
            logger.error(f"Error occured durring JWT token decoding. Error {e}")
        return None

    @classmethod
    def sign_token(cls, token_type: str, **kwargs) -> str:
        payload = {
            "exp": t.time() + 60 * int(cls.TOKEN_EXPIRES.get(token_type)),
            **kwargs,
        }
        token = jwt.encode(
            payload,
            cls.TOKEN_TYPES.get(token_type),
            algorithm=cls.JWT_ALGORITHM,
        )
        return token

    @classmethod
    async def sign_access_token(cls, user_id: int) -> str:
        access_payload = {
            "user_id": user_id,
        }
        access_token = cls.sign_token("access", **access_payload)
        return access_token

    @classmethod
    async def sign_refresh_token(cls, user_id: int) -> str:
        refresh_payload = {"user_id": user_id}
        refresh_token = cls.sign_token("refresh", **refresh_payload)
        await RefreshTokenCache().create(
            user_id=user_id, refresh_token=refresh_token
        )

        return refresh_token

    @classmethod
    async def make_auth_tokens(cls, user_id: int):
        tokens = await AuthHandler.signJWT(user_id)
        return tokens

    @classmethod
    async def delete_refresh_token(cls, user_id: int, refresh_token: str):
        return await RefreshTokenCache().delete_token(user_id, refresh_token)

    @classmethod
    async def delete_user_refresh_tokens(cls, user_id: int):
        return await RefreshTokenCache().delete_user(user_id)
