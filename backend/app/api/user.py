from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.common.response import Response
from app.models.user import User
from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse, UserUpdateRequest, PasswordUpdateRequest
from app.services import user_service



router = APIRouter(prefix="/user", tags=["用户信息的接口"])

@router.get("/me")
def get_user_info(current_user:User = Depends(get_current_user)):
    """获取当前用户信息"""
    return Response.success(data=user_service.get_user_info(current_user))



#更新当前用户信息的接口
@router.put("/me")
#     current_user:User = Depends(get_current_user) 为了校验token
def update_user_info(data: UserUpdateRequest,
                     current_user:User = Depends(get_current_user),
                     db:Session = Depends(get_db)):
    res= user_service.update_user_info(db,current_user,data)
    return Response.success(data=res)

@router.put("/password")
def update_password(data:PasswordUpdateRequest,
                    current_user:User = Depends(get_current_user),
                    db:Session = Depends(get_db)):
    user_service.update_password(db,current_user,data)
    return Response.success()


@router.get("/list")
def get_user_list(page: int = 1,page_size:int = 10,keywords:str | None=None,
                  current_user:User = Depends(get_current_user),db:Session = Depends(get_db)):
    res = user_service.get_user_page_list(db,page,page_size,keywords)
    return Response.success(data=res)

