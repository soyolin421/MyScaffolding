import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.models.user import User
from app.database.database import Base, engine
from app.api import api
from app.common.exceptions import (BusinessException,
                                   bussiness_exception_handler,
                                   validation_exception_handler,
                                   global_exception_handler, http_exception_handler)

# 创建数据库和数据库表
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(api)

#注册自定义的异常
app.add_exception_handler(BusinessException,bussiness_exception_handler)
app.add_exception_handler(HTTPException,http_exception_handler)
app.add_exception_handler(RequestValidationError,validation_exception_handler)
#全局异常兜底，必须放在最后注册
app.add_exception_handler(Exception,global_exception_handler)


@app.get("/")
def root():
    return {"message": "fastApi正在运行中"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
