"""
request请求工具
"""
import socket
import re
from typing import Mapping


def is_mobile(user_agent: str) -> bool:
    """判断是否是手机"""
    if user_agent is None:
        return False
    user_agent = user_agent.lower()
    mobile_agent_list = ['ipad', 'iphone os', 'midp', 'rv:1.2.3.4', 'ucweb', 'android', 'windows ce',
                         'windows mobile', 'webview', 'mobile', 'iphone']
    for tmp_mobile_agent in mobile_agent_list:
        if re.search(tmp_mobile_agent, user_agent):
            return True
    return False


def is_wechat(user_agent: str) -> bool:
    """判断是否是微信浏览器"""
    return 'micromessenger' in user_agent.lower()


def is_wx_work(user_agent: str) -> bool:
    """判断是否是企业微信浏览器"""
    return 'wxwork' in user_agent.lower()


def is_json(headers: dict | Mapping) -> bool:
    """是否是json请求"""
    if isinstance(headers, dict) or isinstance(headers, Mapping):
        return headers.get('X-Requested-With') == 'XMLHttpRequest' or (
                headers.get('Accept') and 'application/json' in headers.get('Accept').lower())


def is_valid_ipv6_address(ip_address):
    """是否是合法ip6地址"""
    try:
        socket.inet_pton(socket.AF_INET6, ip_address)
        return True
    except socket.error:
        return False


def is_valid_ipv4_address(ip_address):
    """是否是合法ip4地址"""
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False
