from database.models import Bill, Group, GroupMember, Product, User
from database.session import async_session
from sqlalchemy import select, update


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


async def get_user_groups(id):
    async with async_session() as session:
        groups = await session.scalars(select(Group).join(GroupMember).where(GroupMember.member_id == id))

        return list(groups)


async def update_user(user_id, **data_dict):
    async with async_session() as session:
        await session.execute(update(User).where(User.id == user_id).values(**data_dict))
        await session.commit()
