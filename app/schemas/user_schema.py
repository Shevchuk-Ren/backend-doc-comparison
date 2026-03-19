from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Login(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
