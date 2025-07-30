from typing import AsyncGenerator, Annotated, ClassVar, Any
import datetime
from tuneapi import tu
from ssl import create_default_context
from uuid import uuid4

from sqlalchemy import (
    UUID as SQLAlchemyUUID,
    DateTime,
    func,
    FetchedValue,
    NullPool,
    exc,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncAttrs,
    AsyncEngine,
)
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import String, Integer, ForeignKey, MetaData

from fastapi import Request

from artha.settings import settings

# metadata

meta = MetaData()

# column declarations

default_timestamp = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True),
        default=func.timezone("UTC", func.statement_timestamp()),
    ),
]

updated_timestamp = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True),
        default=func.timezone("UTC", func.statement_timestamp()),
        onupdate=func.timezone("UTC", func.statement_timestamp()),
        server_onupdate=FetchedValue(),
    ),
]

pkey_uuid = Annotated[
    SQLAlchemyUUID,
    mapped_column(SQLAlchemyUUID(), primary_key=True, default=uuid4),
]

fkey_uuid = Annotated[
    SQLAlchemyUUID,
    mapped_column(SQLAlchemyUUID()),
]

uuid_key = Annotated[
    SQLAlchemyUUID,
    mapped_column(SQLAlchemyUUID()),
]


# Define the Base class
class Base(AsyncAttrs, DeclarativeBase):
    metadata: ClassVar = meta
    type_annotation_map: ClassVar = {dict[str, Any]: JSONB}


def db_ssl_context():
    ssl_context = create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = False  # Set to True in production
    return ssl_context


def connect_to_postgres() -> AsyncEngine:
    return create_async_engine(
        str(settings.db_url),
        echo=False,
        echo_pool=True,
        poolclass=NullPool,
        connect_args={"ssl": db_ssl_context()},
    )


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = request.app.state.db_session_factory()

    try:
        yield session
    except Exception as e:
        tu.logger.error(f"Error in db session: {e}")
        await session.rollback()
    else:
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            tu.logger.error(f"Error in db session: {e}")
            await session.rollback()
        finally:
            await session.close()
    finally:
        await session.close()


###### Tables


class Book(Base):
    __tablename__ = "book"

    id: Mapped[pkey_uuid]
    created_at: Mapped[default_timestamp]
    title: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class Chunk(Base):
    __tablename__ = "chunk"

    id: Mapped[pkey_uuid]
    created_at: Mapped[default_timestamp]
    updated_at: Mapped[updated_timestamp | None]
    text: Mapped[str] = mapped_column(String)
    book_id: Mapped[fkey_uuid] = mapped_column(ForeignKey("book.id"))
