from pydantic import BaseModel

from app.schemas.user import UserResponse


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user: UserResponse

# 注册信息
class RegisterRequest(BaseModel):
    username: str
    password: str
    name: str | None = None
