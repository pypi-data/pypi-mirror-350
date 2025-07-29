from enum import Enum


class ApiEnum(str, Enum):
    admin = '管理'
    file_upload = '文件上传'
    read = '查看'
    add = '添加'
    update = '修改'
    delete = '删除'
    list = '列表'
    list_by_page = '分页列表'
    page = '页面'
    json = 'json数据'

