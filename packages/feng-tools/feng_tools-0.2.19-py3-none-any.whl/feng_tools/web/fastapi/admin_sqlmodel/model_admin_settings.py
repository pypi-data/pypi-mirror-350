from sqlmodel.main import FieldInfo

from feng_tools.orm.sqlmodel import BaseModel
from feng_tools.web.fastapi.common.setting.model_admin_settings import ModelAdminSettings


class SqlModelModelAdminSettings(ModelAdminSettings[BaseModel, FieldInfo]):
    pass
