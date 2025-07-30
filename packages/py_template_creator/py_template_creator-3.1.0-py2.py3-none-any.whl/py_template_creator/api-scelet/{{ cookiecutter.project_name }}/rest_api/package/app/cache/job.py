from mrkutil.utilities import random_uuid
from mrkutil.cache import AsyncRedisBase
from package.app.utilities.enum import JobStatusEnum


class AJobCache(AsyncRedisBase):
    def __init__(self):
        super().__init__(key="u_jobs", cache_timeout=3600)

    async def create_job(self):
        key = random_uuid()
        await self.set(key, {"status": JobStatusEnum.PENDING})
        return key

    async def set_progress(self, key, status: JobStatusEnum):
        await self.set(key, {"status": status})

    async def check_job(self, key):
        job = await self.get(key)
        return job
