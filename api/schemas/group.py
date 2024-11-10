from datetime import datetime
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

# REQUESTS


class CreateProductRequest(BaseModel):
    name: str
    price: float
    quantity: float


class GetGroupRequest(BaseModel):
    id: str


class CreateGroupType1Request(BaseModel):
    title: str
    price: int


class CreateGroupType2Request(BaseModel):
    title: str
    products: List[CreateProductRequest]


class CreateGroupType3Request(BaseModel):
    title: str

class GroupDolgRequest(GetGroupRequest):
    ...

class GroupDolgPaymentRequest(GetGroupRequest):
    amount: float

# Responses

class GroupTypeResponse(BaseModel):
    type: str


class GroupResponse(BaseModel):
    id: str
    title: str
    type: str


class CreateGroupResponse(GroupResponse):
    ...


class GroupList(BaseModel):
    groups: List[GroupResponse]
