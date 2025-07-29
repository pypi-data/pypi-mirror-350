from sqlalchemy import Column

from feng_tools.orm.sqlalchemy.base_models import Model
from feng_tools.web.fastapi.common.setting.model_admin_settings import ModelAdminSettings


class SqlalchemyModelAdminSettings(ModelAdminSettings[Model, Column]):
    pass
