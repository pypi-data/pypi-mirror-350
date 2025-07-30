import os


class settings:
    RATE_LIMITER_ENABLED = bool(
        "true" == str(os.getenv("RATE_LIMITER_ENABLED", "true")).lower()
    )
    WORKERS = int(os.getenv("WORKERS", 1))
    APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
    DEVELOP = bool("true" == str(os.getenv("DEVELOP", "false")).lower())
    DATE_TIME_FORMAT = os.getenv("DATE_TIME_FORMAT", "%Y-%m-%dT%H:%M:%S")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    API_ROOT = os.getenv("API_ROOT", "/api")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_SECRET = os.getenv("JWT_SECRET", "TEMPSECRET")
    REFRESH_JWT_SECRET = os.getenv("REFRESH_JWT_SECRET", "TEMPSECRET")
    JWT_EXPIRE = os.getenv("JWT_EXPIRE", 5)
    REFRESH_JWT_EXPIRE = os.getenv("REFRESH_JWT_EXPIRE", 14400)
    LIMITER_REDIS_URI = os.getenv("LIMITER_REDIS_URI")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*")
    LOCAL_STORE = os.getenv("LOCAL_STORE", "./uploads/")
    UPLOAD_URL_EXPIRE = int(os.getenv("UPLOAD_URL_EXPIRE", 300))
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POOL_SIZE = int(os.getenv("POOL_SIZE", 20))
    # Used by library in background
    ASSET_STORE = os.getenv("ASSET_STORE")
    ASSET_ACCESS_KEY = os.getenv("ASSET_ACCESS_KEY")
    ASSET_SECRET_ACCESS_KEY = os.getenv("ASSET_SECRET_ACCESS_KEY")
    ASSET_LOCATION = os.getenv("ASSET_LOCATION")
    SYNC_ASSETS = bool("true" == str(os.getenv("SYNC_ASSETS", "false")).lower())
    # only used by minio store
    ASSET_PUBLIC_URL = os.getenv("ASSET_PUBLIC_URL")
