from database.models import Bill, BillMember, Group, Product, User
from database.session import async_session
from sqlalchemy import func, select, update


async def create_bill(title, group_id, type) -> Bill:
    async with async_session() as session:
        bill = Bill(title=title, group_id=group_id, type=type)
        session.add(bill)

        await session.commit()
        await session.refresh(bill)

        return bill


async def create_bill_product(bill_id, price, name, quantity):
    async with async_session() as session:
        product = Product(bill_id=bill_id, price=price,
                          name=name, quantity=quantity)
        session.add(product)

        await session.commit()
        await session.refresh(product)

        return product


async def get_bill_product_by_id(id) -> Product:
    async with async_session() as session:
        product = await session.scalar(select(Product).where(Product.id == id))

        return product


async def get_bill_products(bill_id) -> list[Product]:
    async with async_session() as session:
        product = await session.scalars(select(Product).where(Product.bill_id == bill_id))

        return sorted(list(product), key=lambda a: -a.quantity)


async def get_bill_by_id(id) -> Bill:
    async with async_session() as session:
        bill = await session.scalar(select(Bill).where(Bill.id == id))

        return bill


async def join_bill(bill_id, user_id, money=0):
    async with async_session() as session:
        member = BillMember(bill_id=bill_id, member_id=user_id, money=money)
        session.add(member)

        await session.commit()


async def get_bill_member(bill_id, user_id):
    async with async_session() as session:
        group = await session.scalar(select(BillMember).where(BillMember.bill_id == bill_id, BillMember.member_id == user_id))

        return group
    
async def get_bill_members(bill_id):
    async with async_session() as session:
        group = await session.scalars(select(BillMember).where(BillMember.bill_id == bill_id))

        return list(group)


async def bill_dolg_info(bill_id, user_id):
    async with async_session() as session:
        money = await session.execute(select(func.sum(BillMember.money)).where(BillMember.bill_id == bill_id))
        members = await session.scalars(select(BillMember).where(BillMember.bill_id == bill_id))

    return float(money.one()[0]), list(members)


async def update_user_dolg(bill_id, user_id, amount):
    async with async_session() as session:
        member = await session.scalar(select(BillMember).where(BillMember.member_id == user_id, BillMember.bill_id == bill_id))

        if not member:
            raise Exception('No member found')

        await session.execute(update(BillMember).where(BillMember.member_id == user_id, BillMember.bill_id == bill_id).values(dolg=member.dolg + amount))
        await session.commit()

async def update_user_paid_dolg(bill_id, user_id, amount):
    async with async_session() as session:
        member = await session.scalar(select(BillMember).where(BillMember.member_id == user_id, BillMember.bill_id == bill_id))

        if not member:
            raise Exception('No member found')

        await session.execute(update(BillMember).where(BillMember.member_id == user_id, BillMember.bill_id == bill_id).values(paid_dolg=member.paid_dolg + amount))
        await session.commit()


async def update_bill_product(product_id: str, diff: float):
    async with async_session() as session:
        product = await session.scalar(select(Product).where(Product.id == product_id))

        if not product:
            raise Exception('no product found')
        if product.quantity + diff < 0:
            raise Exception('not enough quantity')

        await session.execute(update(Product).where(Product.id == product.id).values(quantity=product.quantity + diff))
        await session.commit()


