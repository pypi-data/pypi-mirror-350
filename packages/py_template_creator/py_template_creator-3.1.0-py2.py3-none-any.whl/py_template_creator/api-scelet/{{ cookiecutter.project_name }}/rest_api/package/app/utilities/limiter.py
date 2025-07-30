from math import ceil
from typing import Callable, Optional, Union, Annotated


from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from starlette.websockets import WebSocket


import redis as pyredis
from pydantic import Field


async def default_identifier(request: Union[Request, WebSocket]):
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0]
    else:
        ip = request.client.host
    return ip + ":" + request.scope["path"]


async def http_default_callback(
    request: Request, response: Response, pexpire: int
):
    """
    default callback when too many requests
    :param request:
    :param pexpire: The remaining milliseconds
    :param response:
    :return:
    """
    expire = ceil(pexpire / 1000)
    raise HTTPException(
        HTTP_429_TOO_MANY_REQUESTS,
        "Too Many Requests",
        headers={"Retry-After": str(expire)},
    )


class FastAPILimiter:
    redis = None
    prefix: Optional[str] = None
    lua_sha: Optional[str] = None
    identifier: Optional[Callable] = None
    http_callback: Optional[Callable] = None
    ws_callback: Optional[Callable] = None
    lua_script = """local key = KEYS[1]
    local limit = tonumber(ARGV[1])
    local expire_time = ARGV[2]

    local current = tonumber(redis.call('get', key) or "0")
    if current > 0 then
    if current + 1 > limit then
    return redis.call("PTTL",key)
    else
            redis.call("INCR", key)
    return 0
    end
    else
        redis.call("SET", key, 1,"px",expire_time)
    return 0
    end"""

    @classmethod
    async def init(
        cls,
        redis,
        prefix: str = "fastapi-limiter",
        identifier: Callable = default_identifier,
        http_callback: Callable = http_default_callback,
        enabled: bool = True,
    ) -> None:
        cls.redis = redis
        cls.prefix = prefix
        cls.identifier = identifier
        cls.http_callback = http_callback
        cls.enabled = enabled
        if enabled:
            cls.lua_sha = await redis.script_load(cls.lua_script)

    @classmethod
    async def close(cls) -> None:
        if cls.enabled:
            await cls.redis.aclose()


class RateLimiter:
    def __init__(
        self,
        times: Annotated[int, Field(ge=0)] = 1,
        milliseconds: Annotated[int, Field(ge=-1)] = 0,
        seconds: Annotated[int, Field(ge=-1)] = 0,
        minutes: Annotated[int, Field(ge=-1)] = 0,
        hours: Annotated[int, Field(ge=-1)] = 0,
        identifier: Optional[Callable] = None,
        callback: Optional[Callable] = None,
    ):
        self.times = times
        self.milliseconds = (
            milliseconds + 1000 * seconds + 60000 * minutes + 3600000 * hours
        )
        self.identifier = identifier
        self.callback = callback

    async def _check(self, key):
        redis = FastAPILimiter.redis
        pexpire = await redis.evalsha(
            FastAPILimiter.lua_sha,
            1,
            key,
            str(self.times),
            str(self.milliseconds),
        )
        return pexpire

    async def __call__(self, request: Request, response: Response):
        if FastAPILimiter.enabled:
            if not FastAPILimiter.redis:
                raise Exception(
                    "You must call FastAPILimiter.init in startup event of fastapi!"
                )
            route_index = 0
            dep_index = 0
            for i, route in enumerate(request.app.routes):
                if (
                    route.path == request.scope["path"]
                    and request.method in route.methods
                ):
                    route_index = i
                    for j, dependency in enumerate(route.dependencies):
                        if self is dependency.dependency:
                            dep_index = j
                            break

            # moved here because constructor run before app startup
            identifier = self.identifier or FastAPILimiter.identifier
            callback = self.callback or FastAPILimiter.http_callback
            rate_key = await identifier(request)
            key = (
                f"{FastAPILimiter.prefix}:{rate_key}:{route_index}:{dep_index}"
            )
            try:
                pexpire = await self._check(key)
            except pyredis.exceptions.NoScriptError:
                FastAPILimiter.lua_sha = await FastAPILimiter.redis.script_load(
                    FastAPILimiter.lua_script
                )
                pexpire = await self._check(key)
            if pexpire != 0:
                return await callback(request, response, pexpire)
