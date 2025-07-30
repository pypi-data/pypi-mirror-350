import datetime
from enum import Enum
from typing import Any, Optional, List

from pydantic import Json, BaseModel
from sqlalchemy import Column

from feng_tools.web.amis.page.AmisPage import AmisPage
from feng_tools.web.fastapi.admin_sqlalchemy.model_admin_settings import SqlalchemyModelAdminSettings
from feng_tools.web.fastapi.common.schema.admin_schemas import AdminAppInfo


class ModelAmisPage(AmisPage):
    def __init__(self, admin_info: AdminAppInfo, settings: SqlalchemyModelAdminSettings):
        self.admin_info = admin_info
        self.settings = settings
        self.model_title = self.settings.model_class.__doc__
        if not self.model_title:
            self.model_title = ''
        if not self.settings.page_title:
            self.settings.page_title = f'{self.model_title}管理'
        self.field_dict ={c.name: c for c in settings.model_class.__table__.columns}
        self.filter_allow_field_dict = self.get_allow_fields(self.field_dict,
                                                                    self.settings.filter_fields,
                                                                    self.settings.list_exclude_fields)
        self.list_allow_field_dict = self.get_allow_fields(self.field_dict,
                                                                  self.settings.list_fields,
                                                                  self.settings.list_exclude_fields)
        self.read_allow_field_dict = self.get_allow_fields(self.field_dict,
                                                                  self.settings.read_fields,
                                                                  self.settings.read_exclude_fields)
        self.add_allow_field_dict = self.get_allow_fields(self.field_dict,
                                                                 self.settings.add_fields,
                                                                 self.settings.add_exclude_fields)
        self.update_allow_field_dict = self.get_allow_fields(self.field_dict,
                                                                    self.settings.update_fields,
                                                                    self.settings.update_exclude_fields)

    def get_allow_fields(self, model_field_dict: dict[str, Column],
                         include_fields: Optional[List[str | Column]] = None,
                         exclude_fields: Optional[list[str]] = None) -> dict[str, Column]:
        """获取模型的允许字段"""
        allow_field_dict = dict()
        for key, field_info in model_field_dict.items():
            if exclude_fields and key in exclude_fields:
                continue
            if include_fields is None:
                allow_field_dict[key] = field_info
            elif len(include_fields) == 0:
                break
            else:
                for tmp_field in include_fields:
                    if not isinstance(tmp_field, str):
                        tmp_field = getattr(tmp_field, 'key')
                    if key == tmp_field:
                        allow_field_dict[key] = field_info
        return allow_field_dict
    def get_form_item(self, field_name:str, field_info:Column, read_only:bool=False)->dict[str, Any]:
        item = {
              "type": "input-text",
              "name": field_name,
              "label": field_info.comment,
        }
        if not field_info.nullable:
            item["required"] = True
        field_type = field_info.type.python_type
        if issubclass(field_type, datetime.datetime):
            item["type"] = "input-datetime"
            item["format"] = "YYYY-MM-DD HH:mm:ss"
        elif issubclass(field_type, datetime.date):
            item["type"] = "input-date"
            item["format"] = "YYYY-MM-DD"
        elif issubclass(field_type, datetime.time):
            item["type"] = "input-time"
            item["format"] = "HH:mm:ss"
        elif issubclass(field_type, bool):
            item["type"] = "checkbox"
        elif issubclass(field_type, int):
            item["type"] = "input-number"
            item["precision"] = 0
        elif issubclass(field_type, float):
            item["type"] = "input-number"
            item["precision"] = 3
        elif issubclass(field_type, (dict, Json)):
            item["type"] = "json-editor"
        elif issubclass(field_type, Enum):
            item["type"] = "select"
            items = [(m.name, m.value) for m in field_type]
            item["options"] = [{"label": label, "value": label} for v, label in items]
            item["extractValue"] =True
            item["joinValues"] =False
        elif issubclass(field_type, str):
            if 'email' in field_name:
                item["type"] = "input-email"
            elif 'password' in field_name or '_pwd' in field_name:
                item["type"] = "input-password"
            elif 'image_url' in field_name or 'img_url' in field_name:
                item["type"] = "input-image"
                item["receiver"]= f"{self.admin_info.api_prefix}/file/upload/image"
        elif issubclass(field_type, BaseModel):
            # pydantic model parse to InputSubForm
            pass
        if item.get("type") == "input-text":
            item["clearable"] = True
            item["clearValueOnEmpty"] = True
        if read_only:
            item['static'] = read_only
        return item

    def get_form_items(self, file_dict:dict[str, Column], read_only:bool=False) -> list[dict[str, Any]]:
        return [self.get_form_item(key, field_info, read_only) for key, field_info in file_dict.items()]

    def get_read_form(self)-> dict[str, Any]:
        return {
            "type": "form",
            "initApi": f"get:{self.admin_info.api_prefix}{self.settings.api_prefix}/item" + "/${id}",
            "body": self.get_form_items(self.read_allow_field_dict, read_only=True),
        }
    def get_add_form(self) -> dict[str, Any]:
        return {
          "type": "form",
          "api": f"post:{self.admin_info.api_prefix}{self.settings.api_prefix}/item",
          "body": self.get_form_items(self.add_allow_field_dict)
        }

    def get_update_form(self):
        return {
            "type": "form",
            "initApi": f"get:{self.admin_info.api_prefix}{self.settings.api_prefix}/item" + "/${id}",
            "api": f"put:{self.admin_info.api_prefix}{self.settings.api_prefix}/item"+"/${id}",
            "body": self.get_form_items(self.update_allow_field_dict)
        }

    @classmethod
    def get_table_column(cls, field_name:str, field_info:Column) -> dict[str, Any]:
        column ={ "name": field_name,
                 "label": field_info.comment,
                  "type": "text"
                 }
        field_type = field_info.type.python_type
        if issubclass(field_type, datetime.datetime):
            column["type"] = "datetime"
        elif issubclass(field_type, datetime.date):
            column["type"] = "date"
        elif issubclass(field_type, datetime.time):
            column["type"] = "text"
        elif issubclass(field_type, bool):
            column["type"] = "status"
        elif issubclass(field_type, Enum):
            column["type"] = "mapping"
            items = [(m.name, m.value) for m in field_type]
            column["map"] = dict()
            for i, (name, value) in enumerate(items):
                column["map"][value]=   f"<span>{value}</span>"
        elif issubclass(field_type, (dict, Json)):
            column["type"] = "json"
        elif issubclass(field_type, str) and ('image_url' in field_name or 'img_url' in field_name):
            column["type"] =  "image"
        return column

    def get_operation_buttons(self)-> list[dict[str, Any]]:
        buttons = list()
        if self.settings.has_read_api:
            buttons.append( {
                "type": "button",
                "label": "详情",
                "actionType": "dialog",
                "icon": "fas fa-eye",
                "tooltip": "查看详情",
                "dialog": {
                    "title": f"查看{self.model_title}",
                    "body": self.get_read_form(),
                    "actions": [
                        {
                            "type": "submit",
                            "label": "确定",
                            "level": "primary"
                        },
                    ]
                },
            },)
        if self.settings.has_update_api:
            buttons.append({
                "type": "button",
                "label": "编辑",
                "tooltip": "修改数据",
                "level": "info",
                "icon": "fas fa-edit",
                "actionType": "dialog",
                "dialog": {
                    "title": f"修改{self.model_title}",
                    "body": self.get_update_form()
                }
            },)
        if self.settings.has_delete_api:
            buttons.append({
                "type": "button",
                "label": "删除",
                "tooltip": "删除数据",
                "level": "danger",
                "icon": "fa fa-times",
                "actionType": "ajax",
                "confirmText": "确认要删除？",
                "api": f"delete:{self.admin_info.api_prefix}{self.settings.api_prefix}/item"+"/${id}"
            })
        return buttons

    def get_table_columns(self)-> list[dict[str, Any]]:
        """获取列表列"""
        columns = [self.get_table_column(key, field_info) for key, field_info in self.list_allow_field_dict.items()]
        columns.append({
            "type": "operation",
            "label": "操作",
            "fixed": "right",
            'headerAlign':'center',
            'align':'center',
            "buttons": self.get_operation_buttons()
        })
        return columns

    def get_table_filter_item(self, field_name:str, field_info:Column) -> dict[str, Any]:
        item = {
              "type": "input-text",
              "name": field_name,
              "label": field_info.comment,
              "clearable": True,
              "placeholder": f"请输入{field_info.comment}",
              "size": "sm"
            }
        field_type = field_info.type.python_type
        if issubclass(field_type, datetime.datetime):
            item["type"] = "input-datetime-range"
            item["format"] = "YYYY-MM-DD HH:mm:ss"
            # 给筛选的 DateTimeRange 添加 today 标签
            item["ranges"] = "today,yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter"
        elif issubclass(field_type, datetime.date):
            item["type"] = "input-date-range"
            item["format"] = "YYYY-MM-DD"
        elif issubclass(field_type, datetime.time):
            item["type"] = "input-time-range"
            item["format"] = "HH:mm:ss"
        elif issubclass(field_type, bool):
            item["type"] = "checkbox"
        elif issubclass(field_type, int):
            item["type"] = "input-number"
            item["precision"] = 0
        elif issubclass(field_type, float):
            item["type"] = "input-number"
            item["precision"] = 3
        elif issubclass(field_type, (dict, Json)):
            item["type"] = "json-editor"
        elif issubclass(field_type, Enum):
            item["type"] = "select"
            items = [(m.name, m.value) for m in field_type]
            item["options"] = [{"label": label, "value": label} for v, label in items]
            item["extractValue"] = True
            item["joinValues"] = False
        elif issubclass(field_type, str):
            if 'email' in field_name:
                item["type"] = "input-email"
            elif 'password' in field_name or '_pwd' in field_name:
                item["type"] = "input-password"
            elif 'image_url' in field_name or 'img_url' in field_name:
                item["type"] = "input-image"
                item["receiver"] = f"{self.admin_info.api_prefix}/file/upload/image"
        elif issubclass(field_type, BaseModel):
            # pydantic model parse to InputSubForm
            pass
        return item
    def get_table_filter_items(self)-> list[dict[str, Any]]:
        return [self.get_table_filter_item(key, field_info) for key, field_info in self.filter_allow_field_dict.items()]
    def get_table_filter(self) -> dict[str, Any]:

        return    {
          # "title": "条件搜索",
          "body": [
            {
              "type": "group",
              "body": self.get_table_filter_items()
            }
          ],
          "actions": [
            {
              "type": "reset",
              "label": "重置"
            },
            {
              "type": "submit",
              "level": "primary",
              "label": "查询"
            }
          ]
        }
    def get_amis_json(self) -> dict[str, Any]:
        """获取amis的配置json"""
        api_prefix_url = f"{self.admin_info.api_prefix}{self.settings.api_prefix}/list"
        filter_field_dict = {
            "page": "${page}",
            "perPage": "${perPage}",
        }
        for key, file_info in self.filter_allow_field_dict.items():
            filter_field_dict[key] = "${" + key + "}"
        amis_json =  {
              "type": "page",
              "title": self.settings.page_title,
              "body":     {
                  "type": "crud",
                  "name": "crud-table",
                  "syncLocation": True,
                  "filter": self.get_table_filter(),
                  "api":{
                    "method": "get",
                    "url": api_prefix_url+"/${page}/${perPage}",
                    "data": filter_field_dict
                  },
                  "headerToolbar": [],
                  "bulkActions": [],
                  "columns": self.get_table_columns()
                }
            }
        if self.settings.has_add_api:
            amis_json["body"]["headerToolbar"].append(
                {
                          "type": "button",
                          "label": "添加",
                          "icon": "fa fa-plus",
                          "actionType": "dialog",
                          "level": "primary",
                          "className": "m-b-sm",
                          "dialog": {
                              "title": f"添加{self.model_title}",
                              "body": self.get_add_form()
                          }
                }
            )
        if self.settings.has_delete_api:
            amis_json["body"]["headerToolbar"].append('bulkActions')
            amis_json["body"]["bulkActions"].append(
                {
                    "type": "button",
                    "label": "批量删除",
                    "icon": "fa fa-trash",
                    "actionType": "ajax",
                    "level": "danger",
                    "confirmText": "确认要删除？",
                    "api": {
                        "method": "post",
                        "url": f"{self.admin_info.api_prefix}{self.settings.api_prefix}" + "/item/delete/batch?ids=${ids|raw}"
                    }
                }
            )
        return amis_json
