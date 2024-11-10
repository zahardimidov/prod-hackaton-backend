# REQUESTS
from datetime import datetime
from typing import List, Optional

from api.schemas.group import CreateProductRequest
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator



# Responses

class BillResponse(BaseModel):
    id: str
    title: str
    group_id: str
    type: str


class CreateBillResponse(BillResponse):
    ...


class ProductResponse(BaseModel):
    id: str
    price: float
    name: str
    quantity: float

class NeedToPay(BaseModel):
    value: float


class ProductListResponse(BaseModel):
    products: List[ProductResponse]


class PaymentUrlResponse(BaseModel):
    url: str


class BillsResponse(BaseModel):
    bills: List[BillResponse]


# REQUESTS


class CreateBillRequest(BaseModel):
    title: str
    group_id: str
    type: str

    products: Optional[List[CreateProductRequest]] = Field(
        None, description='Products')


class SetProductRequest(BaseModel):
    product_id: str
    quantity: float

class SetProducts(BaseModel):
    products: List[SetProductRequest]

class UpdateUserProduct(BaseModel):
    product_id: str


class JoinBillRequest(BaseModel):
    bill_id: str
    money: float


class NeedToPayRequest(BaseModel):
    bill_id: str

class PaymentUrlRequest(BaseModel):
    amount: float
    bills: List[NeedToPayRequest]


