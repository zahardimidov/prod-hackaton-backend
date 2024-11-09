from datetime import datetime

from database.models import BillTypeEnum
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

# REQUESTS


class CreateBillRequest(BaseModel):
    title: str
    type: str
    group_id: str

    amount: int
    date: datetime

    @field_validator("type", mode='before')
    def validate_type(cls, value: str):
        types = [i.value for i in BillTypeEnum]

        if value in types:
            return value
        raise HTTPException(
            status_code=400, detail=f"Type should be in {str(types)}")


# Responses

class BillResponse(BaseModel):
    id: str
    title: str

    group_id: str
    payer_id: str

    amount: int
    type: str
    date: datetime


class CreateBillResponse(BillResponse):
    ...
