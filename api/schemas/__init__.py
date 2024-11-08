from api.schemas.users import *

class DetailResponse(BaseModel):
    detail: str

class ErrorResponse(BaseModel):
    detail: str
