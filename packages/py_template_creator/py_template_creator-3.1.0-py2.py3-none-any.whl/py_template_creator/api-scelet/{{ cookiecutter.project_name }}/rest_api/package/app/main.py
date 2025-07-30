from package.app import settings
import inspect
import logging
import uvicorn
from fastapi.middleware import Middleware
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from package.app.schemas import (
    BaseResponseSchema,
    ValidationErrorResponseSchema,
)
import redis.asyncio as redis
from package.app import api as a_app
from package.app.utilities import CustomHTTPException, FastAPILimiter
from package.app.models import close_db_connection

log_level = settings.LOG_LEVEL
develop = settings.DEVELOP

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    # Formatters define how logs appear
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        }
    },
    # Handlers define where logs are sent (console, file, etc.)
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": log_level,
        }
    },
    # Loggers define logging behavior for different parts of the app
    "loggers": {
        "multipart": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "main": {"level": log_level, "handlers": ["console"]},
        "app": {"level": log_level, "handlers": ["console"]},
        "package": {"level": log_level, "handlers": ["console"]},
        "uvicorn": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "mrkutil": {"level": log_level, "handlers": ["console"]},
    },
    # Root logger (fallback for anything not explicitly defined above)
    "root": {"handlers": ["console"], "level": log_level},
}


logging.config.dictConfig(logging_config)
logger = logging.getLogger("main")

API_STR = settings.API_ROOT


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    redis_connection = redis.from_url(
        settings.LIMITER_REDIS_URI, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(
        redis_connection, enabled=settings.RATE_LIMITER_ENABLED
    )
    yield
    await FastAPILimiter.close()
    await close_db_connection()


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    # Will return errors as same as django
    errors = {}
    message = "Validation error"
    for item in exc.errors():
        item_key = ".".join(
            [
                str(k)
                for k in item["loc"]
                if str(k) not in ["body", "query", "path"]
            ]
        )
        if item_key not in errors:
            errors[item_key] = []
        errors[item_key].append(item["msg"])
        if not item_key:
            item_key = "__all__"
        if not item_key and len(exc.errors()) == 1:
            message = item["msg"]
            break
        errors[item_key] = item["msg"]
    error_res = ValidationErrorResponseSchema(errors=errors, message=message)
    return JSONResponse(
        content=jsonable_encoder(error_res),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    errors = {"message": exc.detail}
    error_res = BaseResponseSchema(**errors)
    return JSONResponse(
        content=jsonable_encoder(error_res),
        status_code=exc.status_code,
    )


async def custom_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "errors": exc.errors,
            "special_code": exc.special_code,
        },
    )


allowed_hosts = settings.ALLOWED_HOSTS
if allowed_hosts != "*":
    allowed_hosts = allowed_hosts.split(",")


async def exception_handler(request: Request, exc: Exception):
    response = JSONResponse(
        content={"message": "Internal server error."}, status_code=500
    )

    origin = request.headers.get("origin")

    if origin:
        # Have the middleware do the heavy lifting for us to parse
        # all the config, then update our response headers
        cors = CORSMiddleware(
            app=app,
            allow_origins=allowed_hosts,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Logic directly from Starlette's CORSMiddleware:
        # https://github.com/encode/starlette/blob/master/starlette/middleware/cors.py#L152

        response.headers.update(cors.simple_headers)
        has_cookie = "cookie" in request.headers

        # If request includes any cookie headers, then we must respond
        # with the specific origin instead of '*'.
        if cors.allow_all_origins and has_cookie:
            response.headers["Access-Control-Allow-Origin"] = origin

        # If we only allow specific origins, then we have to mirror back
        # the Origin header in the response.
        elif not cors.allow_all_origins and cors.is_allowed_origin(
            origin=origin
        ):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers.add_vary_header("Origin")
    return response


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
]

app = FastAPI(
    lifespan=lifespan,
    middleware=middleware,
    debug=develop,
    swagger_ui_parameters={"persistAuthorization": True},
    exception_handlers={
        RequestValidationError: validation_exception_handler,
        CustomHTTPException: custom_exception_handler,
        HTTPException: http_exception_handler,
        Exception: exception_handler,
    },
    responses={
        404: {"model": BaseResponseSchema},
        422: {
            "description": "Validation Error",
            "model": ValidationErrorResponseSchema,
        },
    },
)


for name, obj in inspect.getmembers(a_app):
    if "_router" in name:
        app.include_router(obj, prefix=API_STR)


def dev():
    uvicorn.run(
        "package.app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level=log_level.lower(),
        log_config=logging_config,
        # reload_dirs=["./"],
    )


def prod():
    uvicorn.run(
        "package.app.main:app",
        headers=[
            ("server", "Apache"),
            ("X-Frame-Options", "SAMEORIGIN"),
            ("X-XSS-Protection", "1; mode=block"),
            ("X-Content-Type-Options", "nosniff"),
            (
                "Strict-Transport-Security",
                "max-age=15768000; includeSubDomains",
            ),
            ("Referrer-Policy", "no-referrer-when-downgrade"),
            ("Content-Security-Policy", "frame-ancestors 'self'"),
        ],
        host="0.0.0.0",
        port=8080,
        workers=settings.WORKERS,
        log_level=log_level.lower(),
        log_config=logging_config,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    logger.info("Rest API application up and running!")
    dev() if develop else prod()
