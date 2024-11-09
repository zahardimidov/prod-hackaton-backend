from datetime import datetime

from fastapi import HTTPException
from database.models import BillTypeEnum
from pydantic import BaseModel, Field, field_validator

# REQUESTS

class GetGroupRequest(BaseModel):
    id: str

class CreateGroupRequest(BaseModel):
    title: str

### Responses

class GroupResponse(BaseModel):
    id: str
    title: str

class CreateGroupResponse(GroupResponse):
    ...
