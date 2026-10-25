from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest


def get_user_info(user: User)->UserResponse:
    return UserResponse.model_validate(user)

def update_user_info(db:Session, user:User,data: UserUpdateRequest):
    # 防空的，忽略掉所有是none的属性，pydatic对象转化成字典
    user_dict = data.model_dump(exclude_none=True)
    for field,value in user_dict.items():
        # 一个个将字典里面的值塞到user中
        setattr(user,field,value)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)

