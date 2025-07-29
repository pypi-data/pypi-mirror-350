"""
ip工具类
pip install requests
"""
import requests

def get_ip_info()->None|tuple[str,str,str,str,str,str]:
    """ 获取当前的ip信息
    :return None | (ip, 国家，省，市，区，isp服务商)
        返回值示例：(111.196.215.93,中国,北京,北京,海淀,联通)
    """
    headers = {
        'origin': 'https://ip.cn',
        'referer': 'https://ip.cn/',
        'upgrade-insecure-requests': '1',
        'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136","Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=0, i',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
    }
    response = requests.get('https://my.ip.cn/json/', headers=headers)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        json_resp = response.json()
        if json_resp.get('code') == 0:
            json_data = json_resp.get('data')
            return json_data.get('ip'), json_data.get('country'), json_data.get('province'), json_data.get(
                'city'), json_data.get('district'), json_data.get('isp')
    return None


if __name__ == '__main__':
    print(get_ip_info())