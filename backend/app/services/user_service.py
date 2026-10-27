from operator import or_

from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.common.response import PageResponse
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest, PasswordUpdateRequest, UserCreateRequest
from app.utils.password import verify_password, hash_password


def get_user_info(user: User) -> UserResponse:
    return UserResponse.model_validate(user)

# 修改个人信息
def update_user_info(db: Session, user: User, data: UserUpdateRequest):
    # 防空的，忽略掉所有是none的属性，pydatic对象转化成字典
    user_dict = data.model_dump(exclude_none=True)
    for field, value in user_dict.items():
        # 一个个将字典里面的值塞到user中
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)

# 修改个人密码
def update_password(db: Session, user: User, data: PasswordUpdateRequest):
    if not verify_password(data.old_password, user.password):
        raise BusinessException(message='原密码不正确')
    if data.new_password == data.old_password:
        raise BusinessException(message='新密码和旧密码一样')
    user.password = hash_password(data.new_password)
    db.commit()


# 分页模糊查询用户列表
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

# 增加新用户
def create_user(db: Session,data:UserCreateRequest):
    exist = db.query(User).filter(User.username == data.username).first()
    if exist:
        raise BusinessException(message="账号已经存在")
    user = User(
        username=data.username,
        password=hash_password(data.password),
        name=data.name,
        role=data.role,
        email=data.email,
        phone=data.phone,
        avatar=data.avatar,
        status=data.status,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    # 把数据库的 User 对象转换成 UserResponse 对象，校验字段类型，结果只包含 UserResponse 定义的字段
    return UserResponse.model_validate(user)

#管理员更新用户
def update_user(db: Session,user_id:int,data:UserUpdateRequest):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise BusinessException(message="用户不存在")
    # 转化成字典
    payload = data.model_dump(exclude_none=True)
    # 赋值属性
    for field, value in payload.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


#管理员是删除用户
def delete_user(db: Session,user_id:int,current_user:User):
    if user_id == current_user.id:
        raise BusinessException(message="你删你自己？？")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise BusinessException(message='用户不存在')
    db.delete(user)
    db.commit()
