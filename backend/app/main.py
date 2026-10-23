import uvicorn
from fastapi import FastAPI
from app.models.user import User
from app.database.database import Base,engine
from app.api import api

#创建数据库和数据库表
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(api)

@app.get("/")
def root():
    return {"message": "fastApi正在运行中"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)









