import os
import re
from pathlib import Path

from DrissionPage import WebPage

# ------ 初始化驱动 ------
page = WebPage()
def sanitize_filename(url: str) -> str:
    """清洗非法文件名"""
    return re.sub(r'[\\/*?:"<>|]', '_', url.split('/')[-1].split('?')[0])

def save_resource(re_search, resource_url, resp_content):
    if re_search:
        save_file = os.path.join(save_path, re_search.group(1))
    else:
        save_file = os.path.join(save_path, sanitize_filename(resource_url))
    if 'https://' in save_file:
        return
    os.makedirs(os.path.dirname(save_file), exist_ok=True)
    with open(save_file, 'wb') as f:
        f.write(resp_content)

def save_html(url, save_path):
    # 保存 HTML
    os.makedirs(save_path, exist_ok=True)
    file_name = sanitize_filename(url) or 'index.html'
    html_resp = page.session.get(url)
    html_resp.encoding = 'utf-8'
    save_file = os.path.join(save_path, sanitize_filename(file_name))
    print('保存：', save_file)
    html_text = html_resp.text
    with open(save_file, 'w', encoding='utf-8') as f:
        f.write(html_text)
    return html_text


def clone_one_page(url:str, save_path:str):
    os.makedirs(save_path, exist_ok=True)
    # 开始监听网络请求（支持过滤特定类型的资源）
    page.listen.start(res_type=['image', 'script', 'xhr'])
    # 打开网页
    page.get(url)
    html_text = save_html(url, save_path)
    # 等待所有请求完成
    page.listen.wait_silent()
    for item_data in page.listen.steps():
        print(f'[{item_data.method}]{item_data.url}')
        resp = item_data.response
        item_file_name = re.escape(item_data.url.rsplit('/', maxsplit=1)[1])
        re_search=re.search(rf'(?:href|src)="([^"]+{item_file_name})"', html_text)
        save_resource(re_search, item_data.url, resp.raw_body.encode('utf-8'))
    # 停止监听
    page.listen.stop()


def clone_page(url: str, save_path:Path):
    page.get(url)
    html_text = save_html(url, save_path)
    # 提取并下载资源
    for tag in page.s_eles('x://link|//script|//img'):
        res_url = tag.attr('href') or tag.attr('src')
        if not res_url:
            continue
        if not res_url.startswith(('http', '//')):
            res_url = f"{base_url}/{res_url.lstrip('/')}"
        res_content = page.session.get(res_url).content
        re_search = re.search(r'(?:href|src)="([^"]+)"', tag.html)
        save_resource(re_search, res_url, res_content)


if __name__ == '__main__':
    # ------ 执行克隆 ------
    base_url = 'https://jx.kmmmha.store/jx11x5.html'
    save_path = Path('./site_clone')
    clone_page(base_url, save_path)

