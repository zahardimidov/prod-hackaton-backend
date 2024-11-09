
from api.auth import get_current_user
from api.schemas import *
from database.models import Bill, GroupMember, MemberStatusEnum, User
from database.requests import (create_bill, get_bill_by_id, get_group_member,
                               join_group)
from fastapi import APIRouter, Depends, Form, HTTPException, Response
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


@router.post('/create', response_model=CreateBillResponse, responses=responses)
async def create_bill_handler(data: CreateBillRequest, current_user: User = Depends(get_current_user)):
    new_bill: Bill = await create_bill(
        title=data.title,
        group_id=data.group_id,
        payer_id=current_user.id,
        amount=data.amount,
        type=data.type,
        date=data.date)

    return new_bill