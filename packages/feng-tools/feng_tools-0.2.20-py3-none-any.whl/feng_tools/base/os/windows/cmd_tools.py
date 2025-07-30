"""
Windows上cmd命令相关工具
"""
from feng_tools.base.os import sh_tools


def run(cmd_str: str) -> list[tuple]:
    """运行CMD命令"""
    result_list = []
    out_list = sh_tools.run(cmd_str)
    if out_list:
        out_list = list(filter(lambda x: True if x else False, out_list))
        for tmp_line in out_list:
            tmp_info_tuple = tuple(filter(lambda x: True if x else False, tmp_line.strip().split(' ')))
            result_list.append(tmp_info_tuple)
    return result_list

