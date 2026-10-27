# 用于jwt token鉴权验证的文件
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.models.user import User
from app.utils.jwt import decode_access_token

from app.database.database import get_db

# 在实际请求中，OAuth2PasswordBearer
# 会从 Authorization: Bearer <token> 提取 token，供 get_current_user 验证。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# 用于jwt token鉴权合法性
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db))->User:
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="登录已经失效请重新登录")
    # 获取到用户id
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="无效的登录凭证")
    #从数据库根据用户id查询用户信息
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="用户不存在，请重新登录")
    if user.status != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="账号被禁用")
    return user

def get_current_admin(current_user: User=Depends(get_current_user)):
    """ 判断JWT token内角色是否为admin"""
    if current_user.role != 'admin':
        raise BusinessException(message='没有权限访问',code=403)
    return current_user

