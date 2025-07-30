# server code here for the backend APIs
from tuneapi import tu
from contextlib import asynccontextmanager

import uvicorn
import asyncio
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_context import request_cycle_context
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from artha import db
from artha.web import books
from artha.settings import settings

# Things for the starting up the app


def _setup_db(app: FastAPI):
    tu.logger.info("Setting up the database")
    db_engine = db.connect_to_postgres()
    session_factory = async_sessionmaker(db_engine, expire_on_commit=False)
    app.state.db_engine = db_engine
    app.state.db_session_factory = session_factory


def _close_db(app: FastAPI):
    tu.logger.info("Closing the database")
    db_engine = app.state.db_engine
    db_engine.dispose()


def create_request_ctx_db_session(session: AsyncSession = Depends(db.get_db_session)):
    data = {"db_session": session}
    with request_cycle_context(data):
        yield


# The app itself


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup
    _setup_db(app)
    yield

    # Cleanup
    _close_db(app)


def get_app():
    app = FastAPI(
        dependencies=[Depends(create_request_ctx_db_session)],
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def read_root():
        return {"message": "Hello, World!"}

    app.include_router(books.router, prefix="/api")

    return app
