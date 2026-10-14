from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Data(Base):
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    data: Mapped[list[int]] = mapped_column(nullable=False)