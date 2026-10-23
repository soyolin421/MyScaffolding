from datetime import datetime
from sqlalchemy.orm import sessionmaker, mapped_column,Mapped,DeclarativeBase
from sqlalchemy import create_engine,DateTime
from app.config import settings


engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)  # 数据库会话链接工厂

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
      db.close()


# 数据库公共字段
class Base(DeclarativeBase):
  id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True,comment="主键id")
  create_time: Mapped[datetime] = mapped_column(DateTime,default=datetime.now,comment="创建时间")
  update_time: Mapped[datetime] = mapped_column(DateTime,default=datetime.now,comment="更新时间")

