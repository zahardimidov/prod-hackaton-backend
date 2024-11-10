from datetime import datetime
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

# REQUESTS


class LoginRequest(BaseModel):
    username: str
    password: str

class LoginByCodeRequest(BaseModel):
    code: str


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=6)
    password: str = Field(..., min_length=6)

    @field_validator("password", mode='before')
    def validate_password(cls, value: str):
        if not any([i.isdigit() for i in value]):
            raise HTTPException(
                status_code=400, detail="Password must include numbers")
        if not any([i.isalpha() for i in value]):
            raise HTTPException(
                status_code=400, detail="Password must include letters")
        return value

class SetCardRequest(BaseModel):
    card: str

    @field_validator("card", mode='before')
    def validate_card(cls, value: str):
        if not value.replace(' ', '').isdigit():
            raise HTTPException(status_code=400, detail='Should be a number')
        
        if not len(value.replace(' ', '')) == 16:
            raise HTTPException(status_code=400, detail='Incorrect card number')
        
        return value
# RESPONSES


class UserResponse(BaseModel):
    username: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UsersList(BaseModel):
    users: List[UserResponse]