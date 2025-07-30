from sqlalchemy import Column, String

from feng_tools.orm.sqlalchemy.base_models import Model


class FileResource(Model):
    """文件资源"""
    __tablename__ = 'file_resource'
    file_id = Column(String(64), comment='文件id', unique=True, nullable=False)
    save_path = Column(String(500),comment='保存路径')
    file_url = Column(String(500),comment='访问url', unique=True, nullable=False)