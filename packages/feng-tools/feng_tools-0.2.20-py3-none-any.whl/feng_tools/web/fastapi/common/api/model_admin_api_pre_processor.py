from pydantic import BaseModel
from sqlalchemy import Engine
from starlette.requests import Request

from feng_tools.web.fastapi.common.api.model_admin_api import ModelAdminApi
from feng_tools.web.fastapi.common.model_value.model_value_transformer import ModelValueTransformer
from feng_tools.web.fastapi.common.model_value.model_value_validator import ModelValueValidator
from feng_tools.web.fastapi.common.setting.model_admin_settings import ModelAdminSettings


class ModelAdminApiPreProcessor(ModelAdminApi):
    """型管理API前置处理器"""

    def __init__(self, db_engine: Engine, model_admin_settings: ModelAdminSettings,
                 value_validator_class: type[ModelValueValidator] = None,
                 value_transformer_class: type[ModelValueTransformer] = None):
        super().__init__(db_engine, model_admin_settings)
        if not value_validator_class:
            value_validator_class = ModelValueValidator
        if not value_transformer_class:
            value_transformer_class = ModelValueTransformer
        self.value_validator_class = value_validator_class
        self.value_transformer_class = value_transformer_class

    def _do_validate_and_transform(self, schema):
        for field_name, field_info in schema.model_fields.items():
            value = getattr(schema, field_name)
            if value is None or value == '':
                continue
            if field_info.json_schema_extra:
                # 校验
                validations = field_info.json_schema_extra.get('validations')
                if validations:
                    for validator in validations:
                        if hasattr(self.value_validator_class, validator):
                            validate_result = getattr(self.value_validator_class, validator)(value)
                            if not validate_result.is_passed:
                                ValueError(validate_result.error_msg)
                # 转换值，如：密码加密
                transformations = field_info.json_schema_extra.get('transformations')
                if transformations:
                    for transformer in transformations:
                        if hasattr(self.value_transformer_class, transformer):
                            setattr(schema, field_name, getattr(self.value_transformer_class, transformer)(value))
    def add_api_process(self, request: Request, schema: BaseModel, **kwargs):
        """添加接口处理"""
        self._do_validate_and_transform(schema)

    def read_api_process(self, request: Request, item_id: int, **kwargs):
        """查看接口处理"""
        pass

    def update_api_process(self, request: Request, item_id: int, schema: BaseModel, **kwargs):
        """更新接口处理"""
        self._do_validate_and_transform(schema)

    def delete_api_process(self, request: Request, item_id: int, **kwargs):
        """删除接口处理"""
        pass
    def delete_batch_api_process(self, request: Request, id_list:list[int], **kwargs):
        """批量删除接口处理"""
        pass
    def list_api_process(self, request: Request, query_schema: BaseModel, **kwargs):
        """列表接口处理"""
        pass

    def list_by_page_api_process(self, request: Request, page_num: int, page_size: int,
                                 query_schema: BaseModel, **kwargs):
        """分页列表接口处理"""
        pass
