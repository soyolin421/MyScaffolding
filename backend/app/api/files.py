import os.path
import shutil
import time
import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.common.exceptions import BusinessException
from app.common.response import Response
from app.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR
from app.schemas.file import FileResponse

router = APIRouter(prefix="/files",tags=["文件管理"])

@router.post("/upload")
def upload(file: UploadFile = File(...)):
    """文件上传的接口"""
    if not file.filename:
        raise BusinessException(message="文件名不能为空")
    # 原始的文件名字
    orignal_name = os.path.basename(file.filename)

    #文件的后缀
    ext = Path(orignal_name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise BusinessException(message=f"不支持{ext}类型文件上传")

    #文件大小的校验
    if file.size and file.size > MAX_FILE_SIZE:
        raise BusinessException(message=f"文件不可超过{MAX_FILE_SIZE//1024//1024}MB")

    # 按当天日期创建上传目录
    folder_name = time.strftime("%Y-%m-%d", time.localtime())
    date_path = UPLOAD_DIR / folder_name
    date_path.mkdir(parents=True, exist_ok=True)

    #设置唯一的文件名称 时间戳+前八位uuid
    disk_name = f"{int(time.time()*1000)}__{uuid.uuid4().hex[:8]}{ext}"
    # 文件存储的路径
    save_path = date_path / disk_name

    # 选择流式存储的方式
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return Response.success(
        data=FileResponse(
            original_name=orignal_name,
            disk_name=disk_name,
            size=file.size,
            url=f"/uploads/{folder_name}/{disk_name}")
    )









