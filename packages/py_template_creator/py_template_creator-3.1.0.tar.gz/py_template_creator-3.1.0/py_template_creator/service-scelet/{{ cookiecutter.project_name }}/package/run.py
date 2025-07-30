from mrkutil.service import run_service
from sharedlib.logging_config import get_logging_config
from package.app import settings
from package.app.models import Session

import logging
import logging.config


def on_message_processing_complete():
    Session.remove()


logging.config.dictConfig(
    get_logging_config(settings.LOG_LEVEL, settings.JSON_FORMAT, False)
)

logger = logging.getLogger("main")

def main():
    run_service(
        develop=settings.DEVELOP,
        exchange=settings.EXCHANGE_{{ cookiecutter.project_name.upper() }},
        exchange_type=settings.EXCHANGE_TYPE_{{ cookiecutter.project_name.upper() }},
        queue=settings.QUEUE_{{ cookiecutter.project_name.upper() }},
        max_threads=settings.MAX_THREADS,
        on_message_processing_complete=on_message_processing_complete,
    )


if __name__ == "__main__":
    main()
