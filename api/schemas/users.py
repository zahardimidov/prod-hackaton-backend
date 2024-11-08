from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

# REQUESTS


class LoginRequest(BaseModel):
    username: str
    password: str


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

# RESPONSES


class UserResponse(BaseModel):
    username: str
    registered_at: datetime


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
