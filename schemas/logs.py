from pydantic import BaseModel


class GetAllResponse(BaseModel):
    user: str
    row: str
    date: str
