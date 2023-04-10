from pydantic import BaseModel


class TriangleRequest(BaseModel):
    row: int
