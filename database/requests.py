from database.models import Group, GroupMember, MemberStatusEnum, User, Bill
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
    
async def update_user(username, **kwargs) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))

        if not user:
            raise Exception('Update user not found')

        user = User(username=username, **kwargs)
        session.add(user)

        await session.commit()
        await session.refresh(user)

        return user


async def get_group_by_id(id) -> Group:
    async with async_session() as session:
        group = await session.scalar(select(Group).where(Group.id == id))
    
        return group


async def create_group(**group_data):
    async with async_session() as session:
        group = Group(**group_data)
        session.add(group)

        await session.commit()
        await session.refresh(group)

        return group


async def update_group(group_id, **data_dict):
    async with async_session() as session:
        await session.execute(update(Group).where(Group.id == group_id).values(**data_dict))
        await session.commit()


async def join_group(group_id, user_id, status=MemberStatusEnum.member):
    async with async_session() as session:
        member = GroupMember(
            group_id=group_id, member_id=user_id, member_status=status)
        session.add(member)

        await session.commit()

async def get_group_member(group_id, user_id):
    async with async_session() as session:
        group = await session.scalar(select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.member_id == user_id))

        return group
    


async def create_bill(title, group_id, payer_id, amount, type, date):
    async with async_session() as session:
        payment = Bill(title = title, group_id = group_id, payer_id = payer_id, amount = amount, type = type, date = date)
        session.add(payment)

        await session.commit()
        await session.refresh(payment)

        return payment
    

async def get_bill_by_id(id) -> Bill:
    async with async_session() as session:
        bill = await session.scalar(select(Bill).where(Bill.id == id))

        return bill