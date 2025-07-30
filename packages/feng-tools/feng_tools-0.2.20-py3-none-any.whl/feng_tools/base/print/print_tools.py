def print_header(title):
    print(f"\n{'='*40}")
    print(f"{title.upper():^40}")
    print(f"{'='*40}")


def print_section(title):
    print(f"\n=== {title} ===")

def print_install_info(module_name:str, install_cmd_list:list[str]):
    print(f"{module_name}t未安装，请先安装{module_name}， 安装命令示例：")
    for tmp_install_cmd in install_cmd_list:
        print(tmp_install_cmd)