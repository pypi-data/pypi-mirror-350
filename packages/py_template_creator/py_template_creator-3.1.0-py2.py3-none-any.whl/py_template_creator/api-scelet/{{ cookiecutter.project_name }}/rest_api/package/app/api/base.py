from fastapi import APIRouter

base_router = APIRouter()


@base_router.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome!"}


@base_router.get("/health", tags=["health"])
async def health() -> dict:
    return {"message": "API is working correctly"}
