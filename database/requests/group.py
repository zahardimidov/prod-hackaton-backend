from database.models import Bill, Group, GroupMember, User
from database.session import async_session
from sqlalchemy import select, update


async def get_group_by_id(id) -> Group:
    async with async_session() as session:
        group = await session.scalar(select(Group).where(Group.id == id))

        return group


async def create_group(title, single):
    async with async_session() as session:
        group = Group(title=title, single=single)
        session.add(group)

        await session.commit()
        await session.refresh(group)

        return group


async def update_group(group_id, **data_dict):
    async with async_session() as session:
        await session.execute(update(Group).where(Group.id == group_id).values(**data_dict))
        await session.commit()


async def join_group(group_id, user_id):
    async with async_session() as session:
        member = GroupMember(group_id=group_id, member_id=user_id)
        session.add(member)

        await session.commit()


async def get_group_member(group_id, user_id):
    async with async_session() as session:
        group = await session.scalar(select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.member_id == user_id))

        return group


async def get_group_members(group_id):
    async with async_session() as session:
        members = await session.scalars(select(User).join(GroupMember).where(GroupMember.group_id == group_id))

        return list(members)


async def get_group_bills(group_id) -> list[Bill]:
    async with async_session() as session:
        groups = await session.scalars(select(Bill).where(Bill.group_id == group_id))

        return list(groups)
