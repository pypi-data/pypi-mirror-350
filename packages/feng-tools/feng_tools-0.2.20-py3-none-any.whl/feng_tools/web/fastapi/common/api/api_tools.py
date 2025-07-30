from typing import Callable, Type, Optional, Sequence

from fastapi import APIRouter, params
from pydantic import BaseModel

from feng_tools.web.fastapi.common.page.model_admin_page import ModelAdminPage
from feng_tools.web.fastapi.common.schema.admin_schemas import AdminAppInfo
from feng_tools.web.fastapi.common.schema.api_response import ApiResponse, ListData, PageListData
from feng_tools.web.fastapi.common.schema.api_schemas import ApiEnum
from feng_tools.web.fastapi.common.setting.model_admin_settings import ModelAdminSettings


class ApiTools:
    """为Model创建基础的api接口"""
    def __init__(self, api_router:APIRouter=None):
        self.router = api_router

    def create_add_api(self,
                       api_callback:Callable[[..., BaseModel], ApiResponse[BaseModel]],
                       return_schema_class:Type[BaseModel],
                       depends:Optional[Sequence[params.Depends]] = None,):
        self.router.add_api_route(
            "/item",
            api_callback,
            methods=["POST"],
            response_model=ApiResponse[return_schema_class],
            dependencies=depends,
            name=ApiEnum.add,
        )
    def create_read_api(self,
                        api_callback:Callable[[..., int], ApiResponse[BaseModel]],
                        return_schema_class: Type[BaseModel],
                       depends:Optional[Sequence[params.Depends]] = None):
        self.router.add_api_route(
            "/item/{item_id}",
            api_callback,
            methods=["GET"],
            response_model=ApiResponse[return_schema_class],
            dependencies=depends,
            name=ApiEnum.read,
        )
        pass
    def create_update_api(self,
                          api_callback:Callable[[..., int, BaseModel], ApiResponse[BaseModel]],
                          return_schema_class: Type[BaseModel],
                       depends:Optional[Sequence[params.Depends]] = None):
        self.router.add_api_route(
            "/item/{item_id}",
            api_callback,
            methods=["PUT", "POST"],
            response_model=ApiResponse[return_schema_class],
            dependencies=depends,
            name=ApiEnum.update,
        )
        pass
    def create_delete_api(self,
                          api_callback:Callable[[..., int], ApiResponse[BaseModel]],
                          return_schema_class: Type[BaseModel],
                       depends:Optional[Sequence[params.Depends]] = None):
        self.router.add_api_route(
            "/item/{item_id}",
            api_callback,
            methods=["DELETE"],
            response_model=ApiResponse[return_schema_class],
            dependencies=depends,
            name=ApiEnum.update,
        )
        pass

    def create_delete_batch_api(self,
                          api_callback:Callable[[..., str], ApiResponse[BaseModel]],
                          return_schema_class: Type[BaseModel],
                       depends:Optional[Sequence[params.Depends]] = None):
        self.router.add_api_route(
            "/item/delete/batch",
            api_callback,
            methods=["POST"],
            response_model=ApiResponse[return_schema_class],
            dependencies=depends,
            name=ApiEnum.update,
        )
        pass

    def create_list_api(self,
                        api_callback:Callable[[..., BaseModel], ApiResponse[ListData[BaseModel]]],
                        return_schema_class: Type[BaseModel],
                       depends:Optional[Sequence[params.Depends]] = None):
        self.router.add_api_route(
            "/list",
            api_callback,
            methods=["GET"],
            response_model=ApiResponse[ListData[return_schema_class]],
            dependencies=depends,
            name=ApiEnum.list,
        )
        pass

    def create_list_by_page_api(self, api_callback:Callable[[...,int,int, BaseModel], ApiResponse[PageListData[BaseModel]]],
                                return_schema_class: Type[BaseModel],
                       depends:Optional[Sequence[params.Depends]] = None):
        self.router.add_api_route(
            "/list/{page_num}/{page_size}",
            api_callback,
            methods=["GET"],
            response_model=ApiResponse[PageListData[return_schema_class]],
            dependencies=depends,
            name=ApiEnum.list_by_page,
        )

    def create_page_api(self, admin_app_info:AdminAppInfo, model_admin_page_class: type[ModelAdminPage],
                        model_admin_settings:ModelAdminSettings):
        model_admin_page = model_admin_page_class(admin_app_info,
                                                  model_admin_settings)
        self.router.add_api_route(
            "/page",
            model_admin_page.get_html_response,
            methods=["GET"],
            name=ApiEnum.page,
        )

    def create_json_api(self, admin_app_info:AdminAppInfo, model_admin_page_class: type[ModelAdminPage],
                        model_admin_settings:ModelAdminSettings):
        model_admin_page = model_admin_page_class(admin_app_info,
                                                  model_admin_settings)
        self.router.add_api_route(
            "/json",
            model_admin_page.get_json_response,
            methods=["GET"],
            name=ApiEnum.json,
        )

