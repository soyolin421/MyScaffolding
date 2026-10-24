from datetime import datetime, timedelta
import jwt
from app.config import settings

""" 创建jwt token"""
def create_access_token(user_id: int) -> str:
    # 设定的时间
    expire = datetime.now() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    # 负载
    payload = {
        "user_id": user_id,
        "exp": expire,  # exp是固定的key
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM)


""" 解析jwt token"""
def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
