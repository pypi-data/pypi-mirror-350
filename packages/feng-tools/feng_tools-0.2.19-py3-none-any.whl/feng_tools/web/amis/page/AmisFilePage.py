import json
from typing import Any

from feng_tools.web.amis.page.AmisPage import AmisPage


class AmisFilePage(AmisPage):
    """通过json文件配置页面"""

    def __init__(self, amis_json_file:str):
        super().__init__()
        self.amis_json_file = amis_json_file

    @classmethod
    def _read_json_file(cls, json_data_file: str, encoding:str="utf8") ->dict[str, Any]:
        """读取json文件"""
        with open(json_data_file, encoding=encoding) as read_f:
            return json.loads(read_f.read())

    def get_amis_json(self) -> dict[str, Any]:
        return self._read_json_file(self.amis_json_file)


if __name__ == '__main__':
    import os
    amis_json = os.path.join(os.path.dirname(__file__), 'chat.json')
    print(amis_json)
    page = AmisFilePage(amis_json_file=amis_json)
    html = page.get_page_html()
    with open('amis.html','w', encoding='utf-8') as f:
        f.write(html)