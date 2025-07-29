from abc import ABC, abstractmethod

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from feng_tools.web.fastapi.common.schema.admin_schemas import AdminAppInfo
from feng_tools.web.fastapi.common.setting.model_admin_settings import ModelAdminSettings


class ModelAdminPage(ABC):

    def __init__(self, admin_info: AdminAppInfo, settings:ModelAdminSettings):
        self.admin_info=admin_info
        self.settings = settings

    @abstractmethod
    def get_json_response(self, request:Request) -> JSONResponse:
        pass

    @abstractmethod
    def get_html_response(self, request:Request) -> HTMLResponse:
        pass