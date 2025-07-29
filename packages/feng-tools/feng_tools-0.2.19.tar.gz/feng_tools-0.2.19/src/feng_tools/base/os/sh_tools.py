"""
操作系统上命令相关工具
"""
import os


def run(cmd, is_print: bool = True) -> list[str]:
    """
    运行命令
    :param cmd: 要执行的命令
    :param is_print: 是否在控制台打印信息
    :return: 命令输出信息
    """
    output = os.popen(cmd)
    output_byte = output.buffer.read()
    try:
        line_list = output_byte.decode('utf-8').split('\n')
    except Exception as ex:
        line_list = output_byte.decode('gbk').split('\n')
    if is_print:
        for tmp_line in line_list:
            print(tmp_line)
    return line_list

if __name__ == '__main__':
    # 执行过滤进程并输出
    run('ps aux | grep tat_agent')


