from sqlmodel import Field

from feng_tools.orm.sqlmodel.base_models import BaseModel


class FileResource(BaseModel, table=True):
    __tablename__ = 'file_resource'
    file_id:str = Field(title='文件id', unique=True, nullable=False)
    save_path:str = Field(title='保存路径')
    file_url:str = Field(title='访问url', unique=True, nullable=False)