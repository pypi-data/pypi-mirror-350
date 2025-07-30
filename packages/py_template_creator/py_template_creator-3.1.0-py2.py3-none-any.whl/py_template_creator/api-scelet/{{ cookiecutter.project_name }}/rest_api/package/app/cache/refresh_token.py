import logging
from mrkutil.cache import AsyncRedisBase
from package.app import settings

logger = logging.getLogger(__name__)


class RefreshTokenCache(AsyncRedisBase):
    def __init__(self):
        super().__init__(
            key="u_refresh_token",
            cache_timeout=60 * int(settings.REFRESH_JWT_EXPIRE),
        )

    async def create(self, user_id: int, refresh_token: str):
        await self.set(str(user_id) + "_" + refresh_token, {"user_id": user_id})

    async def retrieve(self, user_id: int, refresh_token: str):
        return await self.get(str(user_id) + "_" + refresh_token)

    async def search_user(self, user_id: int):
        return await self.search(pattern=str(user_id) + "_*")

    async def delete_user(self, user_id: int):
        return await self.delete_keys(pattern=str(user_id) + "_*")

    async def delete_token(self, user_id: int, refresh_token: str):
        return await self.delete(str(user_id) + "_" + refresh_token)
