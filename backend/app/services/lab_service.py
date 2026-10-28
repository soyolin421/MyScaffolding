from operator import or_
from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.common.response import PageResponse
from app.models.lab import Lab
from app.schemas.lab import LabResponse, LabUpdateRequest, LabCreateRequest



# 分页模糊查询列表
def get_lab_page_list(db: Session, page: int, page_size: int, keywords: str | None = None):
    query = db.query(Lab)
    if keywords:
        # 使用操作符号or_将查询改为使用name和姓名的全模糊匹配 like前放i可以忽略大小写
        query = query.filter(Lab.name.ilike(f"%{keywords}%"))
    total = query.count()
    items = (
        query.order_by(Lab.id.desc())
                      .offset((page - 1) * page_size)
                      .limit(page_size)
                      .all()
             )
    return PageResponse(
        list=[LabResponse.model_validate(item) for item in items], total=total
    )

# 增加
def create_lab(db: Session,data:LabCreateRequest):
    exist = db.query(Lab).filter(Lab.name == data.name).first()
    if exist:
        raise BusinessException(message="实验室已经存在")
    #自动忽略空值
    # 将字典转换为key=value
    lab= Lab(**data.model_dump())
    db.add(lab)
    db.commit()
    db.refresh(lab)
    # 把数据库的 Lab 对象转换成 LabResponse 对象，校验字段类型，结果只包含 LabResponse 定义的字段
    return LabResponse.model_validate(lab)

#管理员更新
def update_lab(db: Session,lab_id:int,data:LabUpdateRequest):
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(message="实验室不存在")
    # 转化成字典
    payload = data.model_dump(exclude_none=True)
    # 赋值属性
    for field, value in payload.items():
        setattr(lab, field, value)
    db.commit()
    db.refresh(lab)
    return LabResponse.model_validate(lab)


#管理员是删除
def delete_lab(db: Session,lab_id:int):
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(message='实验室不存在')
    db.delete(lab)
    db.commit()
