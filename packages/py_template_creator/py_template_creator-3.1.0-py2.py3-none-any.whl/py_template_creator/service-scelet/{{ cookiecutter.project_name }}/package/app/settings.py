import os


class settings:
    DEVELOP = bool("true" == str(os.getenv("DEVELOP", "false")).lower())
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    JSON_FORMAT = bool("true" == str(os.getenv("JSON_FORMAT", "false")).lower())
    EXCHANGE_{{ cookiecutter.project_name.upper() }} = os.getenv("EXCHANGE_{{ cookiecutter.project_name.upper() }}")
    EXCHANGE_TYPE_{{ cookiecutter.project_name.upper() }} = os.getenv("EXCHANGE_TYPE_{{ cookiecutter.project_name.upper() }}")
    QUEUE_{{ cookiecutter.project_name.upper() }} = os.getenv("QUEUE_{{ cookiecutter.project_name.upper() }}")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    MAX_THREADS = int(os.getenv("MAX_THREADS", 10))
