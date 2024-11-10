import json

from api.auth import get_current_user
from api.schemas import *
from database.models import Bill, BillType, GroupMember, User
from database.requests import (bill_dolg_info, create_bill,
                               create_bill_product, get_bill_by_id,
                               get_bill_member, get_bill_product_by_id,
                               get_bill_products, get_group_members, get_bill_members, join_bill, update_bill_product, update_user_dolg, update_user_paid_dolg)
from ext import create_payment_url, scanqrcode
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter(prefix='/bill')
auth_scheme = HTTPBearer()

responses = {
    400: {"model": ErrorResponse}
}


@router.get('/get', response_model=BillResponse)
async def get_bill(id: str):
    bill = await get_bill_by_id(id)

    return bill

@router.get('/members', response_model=UsersList)
async def get_bill(id: str):
    members = await get_bill_members(id)

    return UsersList(users=[ UserResponse(username=i.member.username) for i in members ])


@router.post('/create', response_model=CreateBillResponse, responses=responses)
async def create_bill_handler(data: CreateBillRequest, current_user: User = Depends(get_current_user)):
    if current_user.card == None:
        raise HTTPException(
            status_code=400, detail='You should connect bank card')

    if not current_user.id in [i.id for i in await get_group_members(group_id=data.group_id)]:
        raise HTTPException(
            status_code=400, detail='You are not taking part in this group')
    
    if len(data.products) == 0:
        raise HTTPException(status_code=400, detail='You should provide products')

    amount = 0
    for product in data.products:
        amount += product.price

    new_bill: Bill = await create_bill(
        title=data.title,
        group_id=data.group_id,
        type=data.type)

    await join_bill(bill_id=new_bill.id, user_id=current_user.id, money=amount)

    for product in data.products:
        await create_bill_product(bill_id=new_bill.id, price=product.price, name=product.name, quantity=product.quantity)
    return new_bill


@router.post('/join', responses=responses)
async def handler(data: JoinBillRequest, current_user: User = Depends(get_current_user)):
    await join_bill(bill_id=data.bill_id, user_id=current_user.id, money=data.money)

    return DetailResponse(detail='Successfully joined')


@router.post('/scanqr', response_model=ProductListResponse)
async def create_party_handler(file: UploadFile = File(...)):
    bytes = await file.read()

    res: list = await scanqrcode(file=bytes)

    return JSONResponse(content=jsonable_encoder(dict(
        products=[dict(**i) for i in res]
    )))


@router.post('/set_products', response_model=DetailResponse)
async def handler(data: SetProducts, current_user: User = Depends(get_current_user)):
    for product in data.products:
        _product = await get_bill_product_by_id(id=product.product_id)
        if _product.quantity < product.quantity:
            raise HTTPException(status_code=400, detail='Not enough quantity')
        
    for product in data.products:
        _product = await get_bill_product_by_id(id=product.product_id)
        amount = product.quantity * _product.price

        await update_bill_product(product_id=product.product_id, diff = -product.quantity)
        await update_user_dolg(bill_id=_product.bill_id, user_id=current_user.id, amount=amount)

    return DetailResponse(detail='Successfully saved')

@router.get('/products', response_model=ProductListResponse)
async def handler(bill_id: str):
    products = await get_bill_products(bill_id=bill_id)

    return ProductListResponse(products=[ProductResponse(**i.__dict__) for i in products])


async def calc(bill: Bill, user_id: str):
    if bill.type == BillType.equal:
        bill_member = await get_bill_member(bill_id=bill.id, user_id=user_id)

        bill_money, members = await bill_dolg_info(bill_id=bill.id, user_id=user_id)
        part = bill_money / len(members)

        need_to_pay = max(0, part - bill_member.money - bill_member.paid_dolg)

        return need_to_pay

    if bill.type == BillType.nonequal:
        bill_member = await get_bill_member(bill_id=bill.id, user_id=user_id)
        need_to_pay = max(0, bill_member.dolg - bill_member.money - bill_member.paid_dolg)

        return need_to_pay

@router.post("/dolg", response_model=NeedToPay)
async def handler(data: NeedToPayRequest, current_user: User = Depends(get_current_user)):
    bill = await get_bill(id=data.bill_id)

    if not bill:
        raise HTTPException(status_code=400, detail='Bill not found')
    
    value = await calc(bill=bill, user_id=current_user.id)
    
    return NeedToPay(value=value)


@router.post('/payment', response_model=PaymentUrlResponse)
async def create_payment(data: PaymentUrlRequest, current_user: User = Depends(get_current_user)):
    metadata = []
  
    amount = data.amount
    for bill in data.bills:
        bill_obj = await get_bill_by_id(id = bill.bill_id)
        value = await calc(bill=bill_obj, user_id=current_user.id)

        if amount - value > 0:
            metadata.append(dict(bill_id = bill.bill_id, user_id = current_user.id, amount = value))
            amount -= value
        else:
            metadata.append(dict(bill_id = bill.bill_id, user_id = current_user.id, amount = amount))
            amount = 0

    url = create_payment_url(data.amount, metadata=metadata)

    return PaymentUrlResponse(url=url)
