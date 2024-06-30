from pydantic import BaseModel


class RegisterModel(BaseModel):
    city: str
    username: str
    password: str


class LoginModel(BaseModel):
    username: str
    password: str
