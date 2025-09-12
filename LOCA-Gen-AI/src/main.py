# src/main.py
import uvicorn

from interfaces.api.app_factory import create_app
from interfaces.config.constants import UvicornConfig
from interfaces.config.settings import get_settings


def main():
    app = create_app()
    settings = get_settings()

    uvicorn.run(
        app=app,
        host=UvicornConfig.HOST,
        port=UvicornConfig.PORT,
        workers=UvicornConfig.WORKERS,
        log_level=UvicornConfig.LOG_LEVEL,
        timeout_keep_alive=UvicornConfig.TIMEOUT_KEEP_ALIVE,
        reload=settings.DEBUG
    )


if __name__ == '__main__':
    main()