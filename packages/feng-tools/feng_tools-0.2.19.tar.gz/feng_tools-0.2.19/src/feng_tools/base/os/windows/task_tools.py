"""
Windows上Task相关工具
"""
from feng_tools.base.os.windows import cmd_tools


def run_task_list(task_name: str):
    result_list = []
    out_list = cmd_tools.run(f'tasklist|findstr "{task_name}"')
    for tmp_info_tuple in out_list:
        result_list.append({
            'title': tmp_info_tuple[0],
            'pid': tmp_info_tuple[1],
            'name': tmp_info_tuple[2],
            'session_count': tmp_info_tuple[3],
            'memory_usage': tmp_info_tuple[4] + tmp_info_tuple[5],
        })
    return result_list


def run_task_kill(pid: int | str):
    cmd_tools.run(f' taskkill /F /pid {pid}')


def run_task_kill_by_port(port: int):
    result_list = []
    out_list = cmd_tools.run(f'netstat -anoq|findstr "{port}"')
    for tmp_info_tuple in out_list:
        result_list.append({
            'protocol': tmp_info_tuple[0],
            'local_address': tmp_info_tuple[1],
            'out_address': tmp_info_tuple[2],
            'state': tmp_info_tuple[3],
            'pid': tmp_info_tuple[4],
        })
    for tmp_item in result_list:
        if tmp_item.get('local_address') and tmp_item.get('local_address').endswith(f':{port}'):
            print(f'kill PID[{tmp_item.get("pid")}]')
            cmd_tools.run(f' taskkill /F /pid {tmp_item.get("pid")}')


if __name__ == '__main__':
    for tmp_task in run_task_list('uvicorn'):
        run_task_kill(tmp_task.get('pid'))
    run_task_kill_by_port(port=8000)
