
from api.auth import get_current_user
from api.schemas import *
from database.models import BillType, Group, User
from database.requests import (create_bill, create_bill_product, create_group,
                               get_group_bills, get_group_by_id,
                               get_group_member, get_group_members,
                               get_user_groups, join_bill, join_group)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from api.bill import calc, create_payment

router = APIRouter(prefix='/group')
auth_scheme = HTTPBearer()

responses = {
    400: {"model": ErrorResponse}
}


@router.get('/get', response_model=GroupResponse)
async def handler(id: str):
    group = await get_group_by_id(id)
    t = await get_group_type(group)

    return GroupResponse(id=group.id, title=group.title, type=t)


async def get_group_type(group: Group):
    if group.single:
        bills = await get_group_bills(group_id=group.id)

        return bills[0].type
    return 'group'


@router.get('/get_type', response_model=GroupTypeResponse)
async def handler(id: str):
    group = await get_group_by_id(id)
    t = await get_group_type(group)

    return GroupTypeResponse(type=t)


@router.get("/my", response_model=GroupList, responses=responses)
async def handler(current_user: User = Depends(get_current_user)):
    groups = []
    for group in await get_user_groups(id=current_user.id):
        t = await get_group_type(group)
        groups.append(GroupResponse(id=group.id, title=group.title, type=t))

    return GroupList(groups=groups)


@router.get('/bills', response_model=BillsResponse)
async def handler(group_id: str):
    bills = await get_group_bills(group_id=group_id)

    return BillsResponse(bills=[BillResponse(**i.__dict__) for i in bills])


@router.get('/members', response_model=UsersList)
async def handler(group_id: str):
    users = await get_group_members(group_id=group_id)

    return UsersList(users=[UserResponse(**i.__dict__) for i in users])


@router.post('/create_equal', response_model=GroupResponse, responses=responses)
async def handler(data: CreateGroupType1Request, current_user: User = Depends(get_current_user)):
    if current_user.card == None:
        raise HTTPException(
            status_code=400, detail='You should connect bank card')
    new_group: Group = await create_group(title=data.title, single=True)
    await join_group(group_id=new_group.id, user_id=current_user.id)

    bill = await create_bill(title=data.title, group_id=new_group.id, type=BillType.equal)
    await join_bill(bill_id=bill.id, user_id=current_user.id, money=data.price)

    await create_bill_product(bill_id=bill.id, price=data.price, name=data.title, quantity=1)

    t = await get_group_type(new_group)
    return GroupResponse(id=new_group.id, title=new_group.title, type=t)


@router.post('/create_nonequal', response_model=GroupResponse, responses=responses)
async def handler(data: CreateGroupType2Request, current_user: User = Depends(get_current_user)):
    if current_user.card == None:
        raise HTTPException(
            status_code=400, detail='You should connect bank card')
    new_group: Group = await create_group(title=data.title, single=True)
    await join_group(group_id=new_group.id, user_id=current_user.id)

    amount = 0
    for product in data.products:
        amount += product.price

    bill = await create_bill(title=data.title, group_id=new_group.id, type=BillType.nonequal)
    await join_bill(bill_id=bill.id, user_id=current_user.id, money=amount)

    for product in data.products:
        await create_bill_product(bill_id=bill.id, price=product.price, name=product.name, quantity=product.quantity)

    t = await get_group_type(new_group)
    return GroupResponse(id=new_group.id, title=new_group.title, type=t)


@router.post('/create_summary', response_model=GroupResponse, responses=responses)
async def handler(data: CreateGroupType3Request, current_user: User = Depends(get_current_user)):
    if current_user.card == None:
        raise HTTPException(
            status_code=400, detail='You should connect bank card')

    new_group: Group = await create_group(title=data.title, single=False)
    await join_group(group_id=new_group.id, user_id=current_user.id)

    t = await get_group_type(new_group)
    return GroupResponse(id=new_group.id, title=new_group.title, type=t)


@router.post('/join/{group_id}', responses=responses)
async def handler(group_id, current_user: User = Depends(get_current_user)):
    if await get_group_member(group_id=group_id, user_id=current_user.id):
        raise HTTPException(
            status_code=400, detail='You are already taking part in this group')

    await join_group(group_id=group_id, user_id=current_user.id)

    return DetailResponse(detail='Successfully joined')


@router.post("/dolgs", response_model=NeedToPay)
async def handler(data: GroupDolgRequest, current_user: User = Depends(get_current_user)):
    res = 0
    for bill in await get_group_bills(group_id=data.id):
        res += await calc(bill=bill, user_id=current_user.id)
    
    return NeedToPay(value=res)

@router.post("/dolgs/payment", response_model=PaymentUrlResponse)
async def handler(data: GroupDolgPaymentRequest, current_user: User = Depends(get_current_user)):
    bills = await get_group_bills(group_id=data.id)
    res = await create_payment(data = PaymentUrlRequest(amount=data.amount, bills=[NeedToPayRequest(bill_id=i.id) for i in bills]), current_user=current_user)

    return res