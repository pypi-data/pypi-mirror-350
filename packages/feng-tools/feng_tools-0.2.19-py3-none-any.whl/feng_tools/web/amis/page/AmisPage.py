import json
import os.path
from abc import abstractmethod, ABCMeta
from string import Template
from typing import Any

from feng_tools.web.amis.constants import RESOURCE_PATH


class AmisPage(metaclass=ABCMeta):
    default_template_file = os.path.join(RESOURCE_PATH, 'page_template.html')


    @classmethod
    def _read_template_file(cls, template_file: str, encoding="utf8") -> Template:
        """读取模板文件"""
        with open(template_file, encoding=encoding) as f:
            return Template(f.read())

    @abstractmethod
    def get_amis_json(self) -> dict[str, Any]:
        """获取amis的配置json"""
        pass

    def get_page_html(self, template_file: str = None,
                      site_title: str = "fastapi-amis页面",
                      site_icon: str = "",
                      cdn: str = "https://unpkg.com",
                      amis_pkg: str = "amis@6.12.0/sdk",
                      vue_pkg='vue@3.5.13/dist',
                      amis_locale: str = "zh-CN",
                      amis_theme: str = "cxd",
                      self_css_code: str = '',
                      self_js_code: str = '',
                      **kwargs) -> str:
        """获取页面的html代码"""
        if template_file is None:
            template_file = self.default_template_file
        page_template = self._read_template_file(template_file)
        context_dict = {
            "amis_json": json.dumps(self.get_amis_json(), ensure_ascii=False),
            "site_title": site_title,
            "site_icon": site_icon,
            "cdn": cdn,
            "amis_pkg": amis_pkg,
            'vue_pkg': vue_pkg,
            "amis_locale": amis_locale,
            "amis_theme": amis_theme,
            "self_css_code": self_css_code,
            'self_js_code': self_js_code
        }
        context_dict.update(kwargs)
        return page_template.safe_substitute(context_dict)





if __name__ == '__main__':
    print(AmisPage.page_template)
