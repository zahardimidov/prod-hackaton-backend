from sqlalchemy import select

from database.models import User
from database.session import async_session


async def create_user(username, **kwargs) -> User:
    async with async_session() as session:
        user = User(username=username, **kwargs)
        session.add(user)

        await session.commit()
        await session.refresh(user)

        return user


async def get_user_by_id(id) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == id))

        return user
    
async def get_user_by_username(username) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))

        return user


async def update_user(username, **kwargs) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))

        if not user:
            raise Exception('Update user not found')

        for k, v in kwargs.items():
            setattr(user, k, v)

        await session.commit()
        await session.refresh(user)

        return user
