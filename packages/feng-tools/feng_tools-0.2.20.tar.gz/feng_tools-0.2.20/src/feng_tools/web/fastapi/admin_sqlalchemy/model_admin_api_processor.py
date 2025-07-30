import datetime
import math
import traceback
from http.client import HTTPException
from typing import Sequence, Optional, Annotated, Type

from fastapi import params, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import func, Engine, Column, select, and_, delete
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from feng_tools.base.datetime import datetime_tools
from feng_tools.orm.sqlalchemy.base_models import Model
from feng_tools.web.fastapi.admin_sqlalchemy import schema_tools
from feng_tools.web.fastapi.admin_sqlalchemy.model_admin_settings import SqlalchemyModelAdminSettings
from feng_tools.web.fastapi.common.api.api_tools import ApiTools
from feng_tools.web.fastapi.common.api.model_admin_api import ModelAdminApi
from feng_tools.web.fastapi.common.api.model_admin_api_post_processor import ModelAdminApiPostProcessor
from feng_tools.web.fastapi.common.api.model_admin_api_pre_processor import ModelAdminApiPreProcessor
from feng_tools.web.fastapi.common.model_value.model_value_transformer import ModelValueTransformer
from feng_tools.web.fastapi.common.model_value.model_value_validator import ModelValueValidator
from feng_tools.web.fastapi.common.schema.api_response import ApiResponse, PageListData, ListData


def get_model_fields(model_class:type[Model]) -> dict[str, Column]:
    """获取模型所有字段"""
    return {c.name: c for c in model_class.__table__.columns}

class ModelAdminApiProcessor(ModelAdminApi):
    def __init__(self, api_tools: ApiTools, db_engine: Engine, model_admin_settings: SqlalchemyModelAdminSettings,
                 pre_processor_class: type[ModelAdminApiPreProcessor] = None,
                 post_processor_class: type[ModelAdminApiPostProcessor] = None,
                 value_validator_class: type[ModelValueValidator] = None,
                 value_transformer_class: type[ModelValueTransformer] = None):
        super().__init__(db_engine, model_admin_settings)
        self.Session = sessionmaker(bind=self.db_engine)
        self.api_tools = api_tools
        if not pre_processor_class:
            pre_processor_class = ModelAdminApiPreProcessor
        if not post_processor_class:
            post_processor_class = ModelAdminApiPostProcessor
        self.pre_processor = pre_processor_class(db_engine, model_admin_settings,
                                                 value_validator_class=value_validator_class,
                                                 value_transformer_class=value_transformer_class)
        self.post_processor = post_processor_class(db_engine, model_admin_settings)

    def create(self):
        model_class, model_fields, model_schema = self._get_model_infos()
        if self.model_admin_settings.has_add_api:
            self.add_api_process(model_schema)
        if self.model_admin_settings.has_read_api:
            self.read_api_process()
        if self.model_admin_settings.has_update_api:
            self.update_api_process(model_schema)
        if self.model_admin_settings.has_delete_api:
            self.delete_api_process(model_schema)
            self.delete_batch_api_process(model_schema)
        if self.model_admin_settings.has_list_api:
            self.list_api_process()
        if self.model_admin_settings.has_list_by_page_api:
            self.list_by_page_api_process()

    def _get_model_infos(self) -> tuple[Type[BaseModel], dict[str, Column], Type[BaseModel]]:
        model_schema = schema_tools.create_model_schema('ModelSchema',
                                                        self.model_fields,
                                                        schema_fields=self.model_admin_settings.schema_fields,
                                                        exclude_fields=self.model_admin_settings.exclude_fields)
        return self.model_class, self.model_fields, model_schema

    def add_api_process(self,
                        return_schema_class: Type[BaseModel],
                        depends: Optional[Sequence[params.Depends]] = None):
        add_schema = schema_tools.create_model_schema('AddSchema',
                                                      self.model_fields,
                                                      schema_fields=self.model_admin_settings.add_fields,
                                                      exclude_fields=self.model_admin_settings.add_exclude_fields)

        def handle_add_api(request: Request,
                           schema: Annotated[add_schema, Body()]) -> ApiResponse[return_schema_class]:
            self.pre_processor.add_api_process(request=request, schema=schema)
            with self.Session() as session:
                try:
                    model_data = self.model_class(**schema.model_dump())
                    session.add(model_data)
                    session.commit()
                    session.refresh(model_data)
                    # 转换为schema
                    schema_data = return_schema_class.model_validate(model_data.to_dict())
                    return_data = jsonable_encoder(schema_data)
                    self.post_processor.add_api_process(request=request, data=return_data)
                    return ApiResponse(data=return_data)
                except HTTPException as e:
                    session.rollback()
                    print(f'添加接口出现异常：{str(e)}')
                    traceback.print_exc()
                    return ApiResponse(success=False, message="添加失败！服务出现异常，请联系管理员！")

        self.api_tools.create_add_api(handle_add_api,
                                      return_schema_class=return_schema_class,
                                      depends=depends)

    def read_api_process(self, depends: Optional[Sequence[params.Depends]] = None):
        read_schema = schema_tools.create_model_schema('ReadSchema',
                                                       self.model_fields,
                                                       schema_fields=self.model_admin_settings.read_fields,
                                                       exclude_fields=self.model_admin_settings.read_exclude_fields)

        def handle_read_api(request: Request, item_id: int) -> ApiResponse[read_schema]:
            self.pre_processor.read_api_process(request=request, item_id=item_id)
            with self.Session() as session:
                try:
                    db_data = session.get(self.model_class, item_id)
                    if not db_data:
                        return ApiResponse(success=False, message="该条数据不存在！")
                    # 转换为schema
                    schema_data = read_schema.model_validate(db_data.to_dict())
                    return_data = jsonable_encoder(schema_data)
                    self.post_processor.read_api_process(request=request, data=return_data)
                    return ApiResponse(data=return_data)
                except HTTPException as e:
                    print(f'查看接口出现异常：{str(e)}')
                    traceback.print_exc()
                    return ApiResponse(success=False, message="查看失败！服务出现异常，请联系管理员！")

        self.api_tools.create_read_api(handle_read_api,
                                       return_schema_class=read_schema,
                                       depends=depends)

    def update_api_process(self, return_schema_class: Type[BaseModel],
                           depends: Optional[Sequence[params.Depends]] = None):
        update_schema = schema_tools.create_model_schema('UpdateSchema',
                                                         self.model_fields,
                                                         schema_fields=self.model_admin_settings.update_fields,
                                                         exclude_fields=self.model_admin_settings.update_exclude_fields)

        def handle_update_api(request: Request, item_id: int,
                              schema: Annotated[update_schema, Body()]) -> ApiResponse[return_schema_class]:
            self.pre_processor.update_api_process(request=request, item_id=item_id, schema=schema)
            with self.Session() as session:
                try:
                    db_data = session.get(self.model_class, item_id)
                    if not db_data:
                        return ApiResponse(success=False, message="该条数据不存在，无法完成修改！")
                    model_data_fields = getattr(type(db_data), "__fields__")
                    no_update_fields = ['id', 'created_at']
                    for key, value in schema.model_dump().items():
                        if key in no_update_fields:
                            continue
                        if key in model_data_fields:
                            setattr(db_data, key, value)
                    db_data.updated_at = datetime.datetime.now()
                    session.add(db_data)
                    session.commit()
                    session.refresh(db_data)
                    # 转换为schema
                    schema_data = return_schema_class.model_validate(db_data.to_dict())
                    return_data = jsonable_encoder(schema_data)
                    self.post_processor.update_api_process(request=request, data=return_data)
                    return ApiResponse(data=return_data)
                except HTTPException as e:
                    session.rollback()
                    print(f'修改接口出现异常：{str(e)}')
                    traceback.print_exc()
                    return ApiResponse(success=False, message="修改失败！服务出现异常，请联系管理员！")

        self.api_tools.create_update_api(handle_update_api,
                                         return_schema_class=return_schema_class,
                                         depends=depends)

    def delete_api_process(self, return_schema_class: Type[BaseModel],
                           depends: Optional[Sequence[params.Depends]] = None):
        def handle_delete_api(request: Request, item_id: int) -> ApiResponse[return_schema_class]:
            self.pre_processor.delete_api_process(request=request, item_id=item_id)
            with self.Session() as session:
                try:
                    db_data = session.get(self.model_class, item_id)
                    if not db_data:
                        return ApiResponse(success=False, message="该条数据不存在，无法完成删除！")
                    session.delete(db_data)
                    session.commit()
                    # 转换为schema
                    schema_data = return_schema_class.model_validate(db_data.to_dict())
                    return_data = jsonable_encoder(schema_data)
                    self.post_processor.delete_api_process(request=request, data=return_data)
                    return ApiResponse(data=return_data)
                except HTTPException as e:
                    session.rollback()
                    print(f'删除接口出现异常：{str(e)}')
                    traceback.print_exc()
                    return ApiResponse(success=False, message="删除失败！服务出现异常，请联系管理员！")

        self.api_tools.create_delete_api(handle_delete_api,
                                         return_schema_class=return_schema_class,
                                         depends=depends)

    def delete_batch_api_process(self, return_schema_class: Type[BaseModel],
                           depends: Optional[Sequence[params.Depends]] = None):
        def handle_delete_batch_api(request: Request, ids: str) -> ApiResponse[return_schema_class]:
            if ids:
                id_list = [int(item) for item in ids.split(',')]
            else:
                return ApiResponse()
            self.pre_processor.delete_batch_api_process(request=request, id_list=id_list)
            with self.Session() as session:
                try:
                    result = session.execute(delete(self.model_class).where(self.model_class.id.in_(id_list)))
                    row_count = result.rowcount
                    session.commit()
                    self.post_processor.delete_batch_api_process(request=request, data=row_count)
                    return ApiResponse(data={'count':row_count})
                except HTTPException as e:
                    session.rollback()
                    print(f'删除接口出现异常：{str(e)}')
                    traceback.print_exc()
                    return ApiResponse(success=False, message="删除失败！服务出现异常，请联系管理员！")

        self.api_tools.create_delete_batch_api(handle_delete_batch_api,
                                         return_schema_class=return_schema_class,
                                         depends=depends)


    def list_api_process(self, depends: Optional[Sequence[params.Depends]] = None):
        list_schema = schema_tools.create_model_schema('ListSchema',
                                                       self.model_fields,
                                                       schema_fields=self.model_admin_settings.list_fields,
                                                       exclude_fields=self.model_admin_settings.list_exclude_fields)
        filter_schema = schema_tools.create_model_schema('FilterSchema',
                                                         self.model_fields,
                                                         schema_fields=self.model_admin_settings.filter_fields,
                                                         required=False)

        def handle_list_api(request: Request,
                            query_schema: Optional[filter_schema] = None) -> ApiResponse[ListData[list_schema]]:
            self.pre_processor.list_api_process(request=request, query_schema=query_schema)
            with self.Session() as session:
                try:
                    query_stmt, total = self._create_query_stmt(query_schema, request, session, filter_schema)
                    data_list = session.scalars(query_stmt).all()
                    #  转换为schema
                    schema_list = [list_schema.model_validate(item.to_dict()) for item in data_list]
                    return_data = ListData(
                        total=total,
                        item_list=schema_list
                    )
                    self.post_processor.list_api_process(request=request, data=return_data)
                    return ApiResponse(data=return_data)
                except HTTPException as e:
                    print(f'查询接口出现异常：{str(e)}')
                    traceback.print_exc()
                    return ApiResponse(success=False, message="查询失败！服务出现异常，请联系管理员！")

        self.api_tools.create_list_api(handle_list_api,
                                       return_schema_class=list_schema,
                                       depends=depends)

    def _create_filter_conditions(self, request: Request, query_schema: Optional[BaseModel],
                                  filter_schema: Type[BaseModel]):
        filter_conditions = []
        field_info_dict = get_model_fields(self.model_class)
        if not query_schema:
            if request.query_params:
                query_dict = dict()
                for query_key, query_value in request.query_params.items():
                    query_value = query_value.strip()
                    if query_value != '' and query_key in field_info_dict:
                        field_type =  field_info_dict.get(query_key).type.python_type
                        if issubclass(field_type, datetime.datetime) or issubclass(field_type,
                                                                                   datetime.date) or issubclass(
                            field_type, datetime.time):
                            if ',' in query_value:
                                datetime_arr = query_value.split(',')
                                filter_conditions.append(
                                    getattr(self.model_class, query_key) >= datetime_tools.parse_(datetime_arr[0]))
                                filter_conditions.append(
                                    getattr(self.model_class, query_key) <= datetime_tools.parse_(datetime_arr[1]))
                            else:
                                query_dict[query_key] = query_value
                        else:
                            query_dict[query_key] = query_value
                if query_dict:
                    query_schema = filter_schema(**query_dict)
        if query_schema:
            for key, value in query_schema.model_dump().items():
                if value is None or value == '':
                    continue
                if isinstance(value, str):
                    value = value.strip()
                    filter_conditions.append(getattr(self.model_class, key).ilike(f'%{value}%'))
                else:
                    filter_conditions.append(getattr(self.model_class, key) == value)
        return filter_conditions

    def _create_query_stmt(self, query_schema, request, db_session, filter_schema: Type[BaseModel]):
        conditions = self._create_filter_conditions(request, query_schema, filter_schema)
        # 查询总数
        total_query_stmt = select(func.count()).select_from(self.model_class)
        if conditions:
            total_query_stmt = total_query_stmt.where(and_(*conditions))
        total = db_session.execute(total_query_stmt).scalar_one_or_none()
        # 查询数据
        query_stmt = select(self.model_class)
        if conditions:
            query_stmt = query_stmt.where(and_(*conditions))
        query_stmt = query_stmt.order_by(self.model_class.created_at.desc())
        return query_stmt, total

    def list_by_page_api_process(self, depends: Optional[Sequence[params.Depends]] = None):
        list_schema = schema_tools.create_model_schema('ListSchema',
                                                       self.model_fields,
                                                       schema_fields=self.model_admin_settings.list_fields,
                                                       exclude_fields=self.model_admin_settings.list_exclude_fields)
        filter_schema = schema_tools.create_model_schema('FilterSchema',
                                                         self.model_fields,
                                                         schema_fields=self.model_admin_settings.filter_fields,
                                                         required=False)

        def handle_list_api(request: Request, page_num: int, page_size: int,
                            query_schema: Optional[filter_schema] = None) -> ApiResponse[PageListData[list_schema]]:
            self.pre_processor.list_by_page_api_process(request=request,
                                                        page_num=page_num, page_size=page_size,
                                                        query_schema=query_schema)
            with self.Session() as session:
                try:
                    # 构建查询条件
                    query_stmt, total = self._create_query_stmt(query_schema, request, session, filter_schema)
                    query_stmt = query_stmt.offset((page_num - 1) * page_size).limit(page_size)
                    data_list = session.scalars(query_stmt).all()
                    #  转换为schema
                    schema_list = [list_schema.model_validate(item.to_dict()) for item in data_list]
                    return_data = PageListData(
                        page_num=page_num,
                        page_size=page_size,
                        total=total,
                        page_count=math.ceil(total / page_size),
                        item_list=schema_list
                    )
                    self.post_processor.list_by_page_api_process(request=request, data=return_data)
                    return ApiResponse(data=return_data)
                except HTTPException as e:
                    print(f'查询接口出现异常：{str(e)}')
                    traceback.print_exc()
                    return ApiResponse(success=False, message="查询失败！服务出现异常，请联系管理员！")

        self.api_tools.create_list_by_page_api(handle_list_api,
                                               return_schema_class=list_schema,
                                               depends=depends)
