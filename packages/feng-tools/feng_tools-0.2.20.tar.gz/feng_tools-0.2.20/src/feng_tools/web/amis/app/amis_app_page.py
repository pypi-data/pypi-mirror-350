import json
import os
from typing import Any

from feng_tools.web.amis.app.amis_app_settings import AmisAppSettings
from feng_tools.web.amis.constants import RESOURCE_PATH
from feng_tools.web.amis.utils.amis_utils import amis_templates


class AmisAppPage:
    default_template_file = os.path.join(RESOURCE_PATH, 'app_template.html')

    def __init__(self, settings:AmisAppSettings):
        self.settings = settings
        self.init_none_settings()

    def init_none_settings(self):
        for key, value in self.settings.model_dump().items():
            if value is None:
                setattr(self.settings, key, '')

    def get_amis_json(self) -> dict[str, Any]:
        """获取amis的配置json"""
        return {
          'type': 'app',
          'brandName': self.settings.brand_name,
          'logo': self.settings.logo,
          'header': {
            'type': 'tpl',
            'inline': False,
            'className': 'w-full',
            'tpl': self.settings.page_header,
          },
          'footer': self.settings.page_footer,
          'asideBefore': self.settings.aside_before,
          'asideAfter': self.settings.aside_after,
          'api': self.settings.menu_api,
        }

    def get_page_html(self, **kwargs) -> str:
        """获取页面的html代码"""
        if self.settings.template_file is None:
            self.settings.template_file = self.default_template_file
        page_template = amis_templates(self.settings.template_file)
        context_dict = {
            "amis_json": json.dumps(self.get_amis_json(), ensure_ascii=False),
            "site_title": self.settings.app_page_title,
            "site_icon": self.settings.app_page_icon,
            "cdn": self.settings.cdn,
            "amis_pkg": self.settings.amis_pkg,
            'vue_pkg': self.settings.vue_pkg,
            'history_pkg':self.settings.history_pkg,
            "amis_locale": self.settings.amis_locale,
            "amis_theme":  self.settings.amis_theme,
            "self_css_code": self.settings.self_css_code,
            'self_js_code': self.settings.self_js_code,
        }
        context_dict.update(kwargs)
        return page_template.safe_substitute(context_dict)
