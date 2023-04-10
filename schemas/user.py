from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: str


class UserCreateResponse(BaseModel):
    id: int
    username: str
    email: str


class JwtResponse(BaseModel):
    access_token: str
    token_type: str
