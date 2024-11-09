
from fastapi import APIRouter, Depends, Form, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from api.auth import get_current_user
from api.schemas import *
from database.models import User, Group, GroupMember, MemberStatusEnum
from database.requests import create_group, join_group, get_group_by_id, get_group_member

router = APIRouter(prefix='/group')
auth_scheme = HTTPBearer()

responses = {
    400: {"model": ErrorResponse}
}


@router.get('/get', response_model=GroupResponse)
async def get_group(id: str):
    group = await get_group_by_id(id)

    print(group)
    
    return group

@router.post('/create', response_model=CreateGroupResponse, responses=responses)
async def create_group_handler(data: CreateGroupRequest, current_user: User = Depends(get_current_user)):
    new_group: Group = await create_group(**dict(data))
    await join_group(group_id=new_group.id, user_id=current_user.id, status=MemberStatusEnum.creator)

    return new_group


@router.post('/join/{group_id}', responses=responses)
async def join_group_handler(group_id, current_user: User = Depends(get_current_user)):
    if await get_group_member(group_id=group_id, user_id=current_user.id):
        raise HTTPException(status_code=400, detail='You are already taking part in this group')

    await join_group(group_id=group_id, user_id=current_user.id, status=MemberStatusEnum.member)

    return Response(status_code = 200)


