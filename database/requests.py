from models import Data, async_session
from sqlalchemy import select, update, delete

class DataRequests():

    async def get_all_data():
        async with async_session() as session:
            result = await session.scalars(select(Data))
            return result


    async def get_data_by_id(data_id: int):
        async with async_session() as session:
            result = await session.scalars(select(Data).where(Data.id == data_id))
            return result


    async def create_data(data: list[int]):
        async with async_session() as session:
            new_data = Data(data=data)
            session.add(new_data)
            await session.commit()


    async def update_data(data_id: int, new_data: list[int]):
        async with async_session() as session:
            await session.execute(update(Data).where(Data.id == data_id).values(data=new_data))
            await session.commit()


    async def delete_data(data_id: int):
        async with async_session() as session:
            await session.execute(delete(Data).where(Data.id == data_id))
            await session.commit()