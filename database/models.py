from pathlib import Path

from sqlalchemy import Integer, JSON, URL
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

database_path = Path(__file__).resolve().parent.parent / "db.sqlite3"
engine = create_async_engine(
    URL.create("sqlite+aiosqlite", database=str(database_path))
)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Data(Base):
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[list[int]] = mapped_column(JSON, nullable=False)