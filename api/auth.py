
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.schemas import *
from database.models import User
from database.requests import create_user, get_user_by_id, get_user_by_username
from ext import create_jwt_token, pwd_context, verify_jwt_token

router = APIRouter(prefix='/auth')
auth_scheme = HTTPBearer()

responses = {
    400: {"model": ErrorResponse}
}

@router.post("/register", response_model=DetailResponse, responses=responses)
async def register_user(data: RegisterRequest): #data: RegisterRequest = Form(...)
    if await get_user_by_username(username=data.username):
        raise HTTPException(
            status_code=400, detail='This username is already taken')

    await create_user(username=data.username, password=data.password)

    return DetailResponse(detail='Successfully registered')


@router.post("/login", response_model=LoginResponse, responses=responses)
async def login(data: LoginRequest):
    user = await get_user_by_username(data.username)  # Получите пользователя из базы данных
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    is_password_correct = pwd_context.verify(data.password, user.password)

    if not is_password_correct:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
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


@router.get("/me", response_model=UserResponse, responses=responses)
async def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user
