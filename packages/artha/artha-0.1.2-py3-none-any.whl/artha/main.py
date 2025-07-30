import asyncio
import uvicorn
from fire import Fire

from artha.server import get_app
from artha.settings import settings


def _main():
    print("Welcome to Project अर्थ CLI")


def start_server():
    async def _start_server():
        fastpi_app = get_app()
        config = uvicorn.Config(
            app=fastpi_app,
            host=settings.host,
            port=settings.port,
        )
        fastapi_server = uvicorn.Server(config)

        await asyncio.gather(fastapi_server.serve())

    asyncio.run(_start_server())


def main():
    Fire(
        {
            "cli": _main,
            "serve": start_server,
        }
    )
