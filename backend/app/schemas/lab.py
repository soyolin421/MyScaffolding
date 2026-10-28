from pydantic import BaseModel, ConfigDict


class LabResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    img: str | None = None
    location: str | None =None
    capacity: int
    open_time: str | None =None
    close_time: str | None =None
    status: int

    model_config = ConfigDict(from_attributes=True)

#创建用户
class LabCreateRequest(BaseModel):
    name: str
    description: str | None = None
    img: str | None = None
    location: str | None = None
    capacity: int = 0
    open_time: str | None = None
    close_time: str | None = None
    status: int = 1

# 接收前端的参数，在后台修改
class LabUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    img: str | None = None
    location: str | None = None
    capacity: int | None = None
    open_time: str | None = None
    close_time: str | None = None
    status: int | None = None



