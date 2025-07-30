from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from feng_tools.web.fastapi.admin_sqlalchemy.ModelAmisPage import ModelAmisPage
from feng_tools.web.fastapi.admin_sqlalchemy.model_admin_settings import SqlalchemyModelAdminSettings
from feng_tools.web.fastapi.common.page.model_admin_page import ModelAdminPage
from feng_tools.web.fastapi.common.schema.admin_schemas import AdminAppInfo
from feng_tools.web.fastapi.common.schema.api_response import ApiResponse


class AmisModelAdminPage(ModelAdminPage):

    def __init__(self,  admin_info: AdminAppInfo , settings: SqlalchemyModelAdminSettings,):
        super().__init__(admin_info, settings)
        self.amis_page = ModelAmisPage(admin_info, settings)

    def get_json_response(self, request: Request) -> JSONResponse:
        return JSONResponse(content=ApiResponse(
            data=self.amis_page.get_amis_json()
        ).model_dump())

    def get_html_response(self, request: Request) -> HTMLResponse:
        return HTMLResponse(content=self.amis_page.get_page_html())