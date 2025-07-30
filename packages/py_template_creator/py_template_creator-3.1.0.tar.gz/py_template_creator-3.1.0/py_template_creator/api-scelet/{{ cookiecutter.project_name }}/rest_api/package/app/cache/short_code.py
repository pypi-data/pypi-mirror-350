import logging
from mrkutil.cache import AsyncRedisBase
import random
from package.app import settings

logger = logging.getLogger(__name__)


class ShortCode(AsyncRedisBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create(self, data):
        unique = False
        while not unique:
            short_code = str(random.randint(100000, 999999))
            exists = await self.get(short_code)
            if not exists:
                unique = True
                await self.set(short_code, data)
        return short_code

    async def retrieve(self, short_code, delete=True):
        data = await self.get(short_code)
        if data and delete:
            await self.delete(short_code)
        return data


class EmailShortCode(ShortCode):
    def __init__(self):
        super().__init__(
            key="u_short_code_mail",
            cache_timeout=60 * int(settings.SHORT_CODE_EXPIRE),
        )


class PhoneShortCode(ShortCode):
    def __init__(self):
        super().__init__(
            key="u_short_code_phone",
            cache_timeout=60 * int(settings.SHORT_CODE_EXPIRE),
        )
