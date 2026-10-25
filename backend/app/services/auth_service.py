from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.schemas.user import UserResponse
from app.utils.jwt import create_access_token
from app.utils.password import verify_password, hash_password


def login(db: Session, data: LoginRequest):
    # 根据用户账号查询信息
    user = db.query(User).filter(User.username == data.username).first()
    # 判断账号密码是否正确
    if not user or not verify_password(data.password, user.password):
        raise BusinessException(message="账号或密码错误")
    # 验证账号状态
    if user.status != 1:
        raise BusinessException(message="账号被禁用")
    # 创建token
    token = create_access_token(user.id)

    return LoginResponse(token=token, user=UserResponse.model_validate(user))


def register(db: Session, data: RegisterRequest):
    # 根据用户账号查询信息
    user = db.query(User).filter(User.username == data.username).first()
    if user:
        raise BusinessException(message="账号已经存在")
    user_model = User(
        username=data.username,
        password=hash_password(data.password),
        name=data.name or data.username,
        role="student",
        status=1
    )
    db.add(user_model)
    db.commit()
    # 更新用户id
    db.refresh(user_model)
