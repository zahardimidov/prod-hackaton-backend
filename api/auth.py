
from random import randint

from api.schemas import *
from database.models import User
from database.requests import (create_user, get_group_by_id, get_user_by_id,
                               get_user_by_username, update_user, join_group)
from ext import create_jwt_token, pwd_context, verify_jwt_token
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter(prefix='/auth')
auth_scheme = HTTPBearer()

responses = {
    400: {"model": ErrorResponse}
}


@router.post("/register", response_model=DetailResponse, responses=responses)
# data: RegisterRequest = Form(...)
async def register_user(data: RegisterRequest):
    if await get_user_by_username(username=data.username):
        raise HTTPException(
            status_code=400, detail='This username is already taken')

    await create_user(username=data.username, password=data.password)

    return DetailResponse(detail='Successfully registered')


@router.post("/login", response_model=LoginResponse, responses=responses)
async def login(data: LoginRequest):
    # Получите пользователя из базы данных
    user = await get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    is_password_correct = pwd_context.verify(data.password, user.password)

    if not is_password_correct:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    jwt_token = create_jwt_token({"sub": user.id})
    return LoginResponse(access_token=jwt_token)


@router.post("/code", response_model=LoginResponse, responses=responses)
async def handler(data: LoginByCodeRequest):
    group = await get_group_by_id(id=data.code)

    if not group:
        raise HTTPException(status_code=400, detail='Group not found')

    user = await create_user(username=f'Guest {randint(1, 1000)}', password='qwerty')
    await join_group(group_id=group.id, user_id=user.id)
    jwt_token = create_jwt_token({"sub": user.id})

    return LoginResponse(access_token=jwt_token)


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    decoded_data = verify_jwt_token(token.credentials)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = await get_user_by_id(decoded_data["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user


user_router = APIRouter(prefix='/users')


@user_router.get("/me", response_model=UserResponse, responses=responses)
async def handler(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.post("/set_card", responses=responses)
async def handler(data: SetCardRequest, current_user: User = Depends(get_current_user)):
    await update_user(user_id=current_user.id, card=data.card)

    return DetailResponse(detail='Card was saved')
