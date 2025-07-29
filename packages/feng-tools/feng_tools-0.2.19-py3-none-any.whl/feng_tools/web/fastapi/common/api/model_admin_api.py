from abc import ABC, abstractmethod

from sqlalchemy import Engine
try:
    from feng_tools.orm.sqlmodel import model_tools
    from feng_tools.web.fastapi.admin_sqlmodel.model_admin_settings import SqlModelModelAdminSettings
    is_sqlmodel = True
except ImportError:
    is_sqlmodel = False
from feng_tools.web.fastapi.common.setting.model_admin_settings import ModelAdminSettings


class ModelAdminApi(ABC):
    def __init__(self, db_engine:Engine, model_admin_settings: ModelAdminSettings):
        self.db_engine = db_engine
        self.model_admin_settings = model_admin_settings
        self.model_class = model_admin_settings.model_class
        if is_sqlmodel and isinstance(model_admin_settings, SqlModelModelAdminSettings):
            self.model_fields = model_tools.get_model_fields(self.model_class)
        else:
            self.model_fields = {c.name: c for c in self.model_class.__table__.columns}

    @abstractmethod
    def add_api_process(self, **kwargs):
        """添加接口处理"""
        pass

    @abstractmethod
    def read_api_process(self, **kwargs):
        """查看接口处理"""
        pass

    @abstractmethod
    def update_api_process(self, **kwargs):
        """更新接口处理"""
        pass

    @abstractmethod
    def delete_api_process(self, **kwargs):
        """删除接口处理"""
        pass
    @abstractmethod
    def delete_batch_api_process(self, **kwargs):
        """批量删除接口处理"""
        pass
    @abstractmethod
    def list_api_process(self, **kwargs):
        """列表接口处理"""
        pass

    @abstractmethod
    def list_by_page_api_process(self, **kwargs):
        """分页列表接口处理"""
        pass
    pass