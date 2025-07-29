import os
from typing import Optional

from pydantic import BaseModel, Field

from feng_tools.web.amis.constants import RESOURCE_PATH

class AmisAppPageSettings(BaseModel):
    app_page_title: Optional[str] = Field('xxx 系统', title='应用页面标题', description='显示在<title>标签中')
    app_page_icon: Optional[str] = Field(None, title='应用页面icon', description='显示在<head>标签中')
    cdn: Optional[str] = Field("https://unpkg.com", title='应用页面使用的cdn', description='js和css引用的cdn')
    amis_pkg: Optional[str] = Field("amis@6.12.0/sdk", title='amis的pkg', description='amis的js和css引用')
    vue_pkg: Optional[str] = Field('vue@3.5.13/dist', title='vue的pkg', description='vue的js和css引用')
    history_pkg: Optional[str] = Field('history@4.10.1/umd', title='history的pkg', description='history的js和css引用')
    amis_locale: Optional[str] = Field("zh-CN", title='amis的语言', description='默认使用中文')
    amis_theme: Optional[str] = Field('cxd', title='amis主题', description='默认使用cxd主题')
    self_css_code: Optional[str] = Field(None, title='自定义引入css的代码', description='示例：<link rel="stylesheet" href="/static/css/custom.css">')
    self_js_code: Optional[str] = Field(None, title='自定义引入js的代码', description='示例：<script src="/static/js/custom.js"></script>')


class AmisAppSettings(AmisAppPageSettings):
    template_file:Optional[str] = os.path.join(RESOURCE_PATH, 'app_template.html')
    brand_name:Optional[str] = Field('xxx系统', title='应用名称', description='显示在菜单栏上，示例：xxx系统')
    logo:Optional[str] = Field(None, title='Logo图片', description='显示在菜单栏上，示例：/public/logo.png')
    page_header:Optional[str] = Field(None, title='页面顶部', description='显示在页面的顶部，示例：<div class="flex justify-between"><div>顶部区域左侧</div><div>顶部区域右侧</div></div>')
    page_footer:Optional[str] = Field(None, title='页面底部', description='显示在页面的底部，如版权信息，示例：<div class="p-2 text-center bg-light">版权所有，侵权必究</div>')
    aside_before :Optional[str] = Field(None, title='菜单上前面区域', description='显示在菜单前面区域，示例：<div class="p-2 text-center">菜单前面区域</div>')
    aside_after:Optional[str] = Field(None, title='菜单下后面区域', description='显示在菜单后面区域，示例：<div class="p-2 text-center">菜单后面区域</div>')
    menu_api: str = Field(title='菜单的api接口', description='用于获取菜单的api接口')



