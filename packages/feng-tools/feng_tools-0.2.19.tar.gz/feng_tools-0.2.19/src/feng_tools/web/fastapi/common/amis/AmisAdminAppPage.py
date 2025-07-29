from starlette.requests import Request
from starlette.responses import HTMLResponse

from feng_tools.web.amis.app.amis_app_page import AmisAppPage
from feng_tools.web.amis.app.amis_app_settings import AmisAppSettings
from feng_tools.web.fastapi.common.page.admin_app_page import AdminAppPage


class AmisAdminAppPage(AdminAppPage):
    def __init__(self, settings: AmisAppSettings):
        self.settings = settings

    def get_html_response(self, request: Request) -> HTMLResponse:
        amis_app_page = AmisAppPage(self.settings)
        return HTMLResponse(content=amis_app_page.get_page_html())

