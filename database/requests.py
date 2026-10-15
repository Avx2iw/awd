from .models import Data, async_session
from .models import Base, engine
from sqlalchemy import delete, select, update


class DataRequests:
    @staticmethod
    async def initialize_database():
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    @staticmethod
    async def get_all_data() -> list[Data]:
        async with async_session() as session:
            result = await session.scalars(select(Data).order_by(Data.id))
            return list(result)

    @staticmethod
    async def get_data_by_id(data_id: int):
        async with async_session() as session:
            result = await session.scalars(select(Data).where(Data.id == data_id))
            return result.first()

    @staticmethod
    async def create_data(data: list[int]):
        async with async_session() as session:
            new_data = Data(data=data)
            session.add(new_data)
            await session.commit()

    @staticmethod
    async def update_data(data_id: int, new_data: list[int]):
        async with async_session() as session:
            await session.execute(update(Data).where(Data.id == data_id).values(data=new_data))
            await session.commit()

    @staticmethod
    async def delete_data(data_id: int):
        async with async_session() as session:
            await session.execute(delete(Data).where(Data.id == data_id))
            await session.commit()