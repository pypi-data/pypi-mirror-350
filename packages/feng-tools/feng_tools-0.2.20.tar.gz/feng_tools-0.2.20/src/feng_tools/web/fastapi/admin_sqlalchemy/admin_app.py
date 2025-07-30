import sys

from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError, ValidationException
from pydantic import ValidationError

from feng_tools.orm.sqlalchemy.sqlalchemy_db_tools import SqlalchemyDbTool
from feng_tools.web.fastapi.admin_sqlalchemy.AmisModelAdminPage import AmisModelAdminPage
from feng_tools.web.fastapi.admin_sqlalchemy.model_admin_api_processor import ModelAdminApiProcessor
from feng_tools.web.fastapi.admin_sqlalchemy.model_admin_settings import SqlalchemyModelAdminSettings
from feng_tools.web.fastapi.common.api.api_tools import ApiTools
from feng_tools.web.fastapi.common.api.model_admin_api_post_processor import ModelAdminApiPostProcessor
from feng_tools.web.fastapi.common.api.model_admin_api_pre_processor import ModelAdminApiPreProcessor
from feng_tools.web.fastapi.common.handler.exception_handler import validation_exception_handle, value_exception_handle, \
    exception_handle
from feng_tools.web.fastapi.common.model_value.model_value_transformer import ModelValueTransformer
from feng_tools.web.fastapi.common.model_value.model_value_validator import ModelValueValidator
from feng_tools.web.fastapi.common.page.model_admin_page import ModelAdminPage
from feng_tools.web.fastapi.common.schema.admin_schemas import AdminAppInfo
from feng_tools.web.fastapi.common.schema.api_response import ApiResponse
from feng_tools.web.fastapi.common.schema.api_schemas import ApiEnum
from feng_tools.web.fastapi.common.setting.admin_app_settings import AdminAppSettings


class AdminApp(FastAPI):

    def __init__(self, settings: AdminAppSettings,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings
        if self.settings.db_engine:
            self.db_engine = self.settings.db_engine
        else:
            if self.settings.database_setting is None or settings.database_setting.url is None:
                print('请配置数据库连接：database_setting')
                sys.exit(1)
            db_tool = SqlalchemyDbTool(settings.database_setting)
            self.db_engine = db_tool.create_engine()
        if hasattr(self.settings.file_handler, 'set_db_engine'):
            self.settings.file_handler.set_db_engine(self.db_engine)

    def register_exception_handlers(self, app: FastAPI):
        for tmp in [app, self]:
            tmp.add_exception_handler(RequestValidationError, handler=validation_exception_handle)
            tmp.add_exception_handler(ValueError, handler=value_exception_handle)
            app.add_exception_handler(ValidationException, handler=value_exception_handle)
            app.add_exception_handler(ValidationError, handler=value_exception_handle)
            tmp.add_exception_handler(Exception, exception_handle)

    def load_app(self, app: FastAPI,
                 admin_prefix: str = None,
                 admin_name: str = "admin",
                 enable_exception_handlers: bool = True):
        if admin_prefix:
            self.settings.prefix = admin_prefix
        app.mount(self.settings.prefix, self, name=admin_name)
        from feng_tools.orm.sqlalchemy.init import Base
        Base.metadata.create_all(self.db_engine)
        if enable_exception_handlers:
            self.register_exception_handlers(app)
        self._create_admin_page()
        self._create_file_api()

    def _create_admin_page(self):
        index_router = APIRouter()
        index_router.add_api_route(
            "/",
            self.settings.admin_app_page.get_html_response,
            methods=["GET"],
            name=ApiEnum.admin,
        )
        self.include_router(index_router)

    def _create_file_api(self):
        file_handler = self.settings.file_handler
        index_router = APIRouter(prefix='/file')
        index_router.add_api_route(
            "/upload/{file_type}",
            file_handler.upload_handle,
            methods=["POST", "PUT"],
            response_model=ApiResponse,
            name=ApiEnum.file_upload,
        )
        index_router.add_api_route(
            "/download/{file_id}",
            file_handler.download_handle,
            methods=["GET"],
            name=ApiEnum.file_upload,
        )
        self.include_router(index_router)

    def _create_model_admin_page(self, api_tools: ApiTools, model_admin_page_class: type[ModelAdminPage],
                                 model_admin_settings: SqlalchemyModelAdminSettings):
        """创建模型的管理页面"""
        if not model_admin_settings.has_page_api:
            return
        if not model_admin_page_class:
            model_admin_page_class = AmisModelAdminPage
        admin_app_info = AdminAppInfo(api_prefix=self.settings.prefix)
        api_tools.create_page_api(admin_app_info, model_admin_page_class, model_admin_settings)
        api_tools.create_json_api(admin_app_info, model_admin_page_class, model_admin_settings)

    def _create_model_admin_api(self, api_tools, model_admin_api_class: type[ModelAdminApiProcessor],
                                model_admin_settings: SqlalchemyModelAdminSettings,
                                pre_processor_class: type[ModelAdminApiPreProcessor] = None,
                                post_processor_class: type[ModelAdminApiPostProcessor] = None,
                                value_validator_class: type[ModelValueValidator] = None,
                                value_transformer_class: type[ModelValueTransformer] = None):
        """创建模型的管理api"""
        if not model_admin_api_class:
            model_admin_api_class = ModelAdminApiProcessor
        model_admin_api = model_admin_api_class(api_tools, self.db_engine, model_admin_settings,
                                                pre_processor_class=pre_processor_class,
                                                post_processor_class=post_processor_class,
                                                value_validator_class=value_validator_class,
                                                value_transformer_class=value_transformer_class)
        model_admin_api.create()

    def register_model_admin(self, model_admin_settings: SqlalchemyModelAdminSettings,
                             model_admin_page_class: type[ModelAdminPage] = None,
                             model_admin_api_class: type[ModelAdminApiProcessor] = None,
                             pre_processor_class: type[ModelAdminApiPreProcessor] = None,
                             post_processor_class: type[ModelAdminApiPostProcessor] = None,
                             value_validator_class: type[ModelValueValidator] = None,
                             value_transformer_class: type[ModelValueTransformer] = None):
        """
        注册模型
        :param model_admin_settings:
        :param model_admin_page_class: model管理页面类（用于生成model的管理页面）
        :param model_admin_api_class: model管理API类（用于生成model的管理页面）
        :param pre_processor_class: 值接收到处理前的处理器类
        :param post_processor_class: 值返回前的处理器类
        :param value_validator_class: 值校验器类
        :param value_transformer_class: 值转换器类
        """
        if not model_admin_settings.api_router:
            if not model_admin_settings.api_prefix:
                raise ValueError(f'请配置模型{model_admin_settings.model_class}的api_prefix')
            model_admin_settings.api_router = APIRouter(prefix=model_admin_settings.api_prefix)
        api_tools = ApiTools(api_router=model_admin_settings.api_router)

        # 创建模型的管理api
        self._create_model_admin_api(api_tools, model_admin_api_class, model_admin_settings,
                                     pre_processor_class=pre_processor_class,
                                     post_processor_class=post_processor_class,
                                     value_validator_class=value_validator_class,
                                     value_transformer_class=value_transformer_class)
        # 创建模型的管理页面
        self._create_model_admin_page(api_tools, model_admin_page_class, model_admin_settings)
        # 添加模型路由到管理app
        self.include_router(model_admin_settings.api_router)
