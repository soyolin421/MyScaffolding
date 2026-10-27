from operator import or_

from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.common.response import PageResponse
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest, PasswordUpdateRequest
from app.utils.password import verify_password, hash_password


def get_user_info(user: User) -> UserResponse:
    return UserResponse.model_validate(user)


def update_user_info(db: Session, user: User, data: UserUpdateRequest):
    # 防空的，忽略掉所有是none的属性，pydatic对象转化成字典
    user_dict = data.model_dump(exclude_none=True)
    for field, value in user_dict.items():
        # 一个个将字典里面的值塞到user中
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


def update_password(db: Session, user: User, data: PasswordUpdateRequest):
    if not verify_password(data.old_password, user.password):
        raise BusinessException(message='原密码不正确')
    if data.new_password == data.old_password:
        raise BusinessException(message='新密码和旧密码一样')
    user.password = hash_password(data.new_password)
    db.commit()


def get_user_page_list(db: Session, page: int, page_size: int, keywords: str | None = None):
    query = db.query(User)
    if keywords:
        User.username.like(f'%{keywords}%')
        # 使用操作符号or_将查询改为使用账号和姓名的全模糊匹配 like前放i可以忽略大小写
        query = query.filter(
            or_(User.username.ilike(f'%{keywords}%'),
                User.name.ilike(f'%{keywords}%')
        )
        )
    total = query.count()
    items = (
        query.order_by(User.id.desc())
                      .offset((page - 1) * page_size)
                      .limit(page_size)
                      .all()
             )
    return PageResponse(
        list=[UserResponse.model_validate(item) for item in items], total=total
    )
