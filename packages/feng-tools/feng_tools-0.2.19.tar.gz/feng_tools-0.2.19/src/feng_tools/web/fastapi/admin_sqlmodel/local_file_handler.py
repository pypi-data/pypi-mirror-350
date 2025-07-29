import logging
import os
import time
import traceback
from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from sqlmodel import Session, select
from starlette.requests import Request
from starlette.responses import FileResponse

from feng_tools.base.id import uuid_tools
from feng_tools.web.fastapi.admin_sqlmodel.admin_models import FileResource
from feng_tools.web.fastapi.common.handler.file_handler import FileHandler
from feng_tools.web.fastapi.common.schema.api_response import ApiResponse


class LocalFileHandler(FileHandler):
    def __init__(self, local_save_path:str):
        self.local_save_path=local_save_path

    def set_db_engine(self, db_engine):
        self.db_engine=db_engine
    def upload_handle(self, request: Request, file_type: str, file: UploadFile) -> ApiResponse:
        # 创建员工专属目录
        upload_dir = os.path.join(self.local_save_path, file_type, datetime.now().date().strftime('%Y%m%d'))
        os.makedirs(upload_dir, exist_ok=True)
        # 生成唯一文件名
        timestamp = int(time.time())
        file_id = f'{uuid_tools.get_uuid32()}{timestamp}'
        filepath = os.path.join(upload_dir, f"{file_id}.jpg")
        # 保存图片文件
        with open(filepath, "wb") as f:
            f.write(file.file.read())
        file_url = f'/admin/file/download/{file_id}'
        with Session(self.db_engine) as session:
            try:
                session.add(FileResource(file_id=file_id,
                                         save_path=filepath,
                                         file_url=file_url))
                session.commit()
                return ApiResponse(data={
                    'file_id':file_id,
                    "filename": file.filename,
                    'url': file_url,
                    'value':file_url,
                })
            except Exception as e:
                session.rollback()
                logging.error(f'文件上传失败！异常：{str(e)}')
                traceback.print_exc()
                return ApiResponse(success=False,message='文件上传失败，请联系管理员！')

    def download_handle(self, request: Request, file_id: str,
                        file_name:Optional[str]=None, download_flag:Optional[bool]=False):
        with Session(self.db_engine) as session:
            smst = select(FileResource).where(FileResource.file_id==file_id)
            file_resource = session.exec(smst).first()
            if not file_resource:
                return ApiResponse(success=False, message="文件不存在！")
        local_file = file_resource.save_path
        response = FileResponse(local_file)
        with open(local_file, "rb") as file:
            if download_flag:
                if file_name is None:
                    file_name = os.path.split(local_file)[1]
                response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
            response.body = file.read()
        return response