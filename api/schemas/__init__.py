from api.schemas.users import *
from api.schemas.group import *
from api.schemas.bill import *

class DetailResponse(BaseModel):
    detail: str

class ErrorResponse(BaseModel):
    detail: str
