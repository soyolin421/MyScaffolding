from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    role: str
    email: str | None =None
    phone: str | None =None
    avatar: str | None =None
    status: int

    model_config = ConfigDict(from_attributes=True)

# 接收前端的参数，在后台修改
class UserUpdateRequest(BaseModel):
    name:str | None = None
    email:str | None = None
    phone:str | None = None
    avatar:str | None = None