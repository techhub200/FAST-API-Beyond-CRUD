from pydantic import BaseModel, EmailStr


class UserCreateModel(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str


class TokenResponseModel(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenRequestModel(BaseModel):
    refresh_token: str

