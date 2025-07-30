import uvicorn
from fastapi import FastAPI

from superlinked.server.app import ServerApp
from superlinked.server.configuration.app_config import AppConfig


def get_app() -> FastAPI:
    return ServerApp().app


if __name__ == "__main__":
    app_config = AppConfig()
    uvicorn.run(
        "superlinked.server.__main__:get_app",
        host=app_config.SERVER_HOST,
        port=app_config.SERVER_PORT,
        workers=app_config.WORKER_COUNT,
        log_config=None,
        factory=True,
    )
