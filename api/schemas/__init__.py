from api.schemas.bill import *
from api.schemas.group import *
from api.schemas.users import *


class DetailResponse(BaseModel):
    detail: str


class ErrorResponse(BaseModel):
    detail: str
