from sqlalchemy import select, insert, update
from sqlalchemy.orm import DeclarativeMeta
from typing import TypeVar,Generic, Type

from src.database import async_session_maker

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)

class BaseService(Generic[ModelType]):
    model: Type[ModelType]

    @classmethod
    async def find_by_id(cls, model_id: int):
        async  with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, filter_by: dict, **data):
        async with async_session_maker() as session:
            query = update(cls.model).where(
                *[getattr(cls.model, key) == value for key, value in filter_by.items()]
            ).values(**data)
            await session.execute(query)
            await session.commit()
