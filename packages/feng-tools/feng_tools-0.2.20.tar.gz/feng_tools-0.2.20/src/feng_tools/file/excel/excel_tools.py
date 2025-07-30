"""
Excel工具
pip install pandas
"""
import os
from io import BytesIO

import pandas as pd
from typing import List, Dict


def export_excel(data: List[Dict], save_excel_file: str) -> bool:
    """
    导出数据到Excel文件
    :param data: 要导出的数据列表（每个元素为一个字典）
    :param save_excel_file: Excel文件路径
    :return: 导出是否成功
    """
    try:
        if not data:
            print("导出失败：数据为空")
            return False

        df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(save_excel_file), exist_ok=True)
        df.to_excel(save_excel_file, index=False, engine='openpyxl')
        return True
    except FileNotFoundError:
        print(f"导出失败：文件路径无效 - {save_excel_file}")
        return False
    except PermissionError:
        print(f"导出失败：没有权限写入文件 - {save_excel_file}")
        return False
    except Exception as e:
        print(f"导出Excel失败: {str(e)}")
        return False


def import_excel(file_path: str) -> List[Dict]:
    """
    从Excel文件导入数据
    :param file_path: Excel文件路径
    :return: 导入的数据列表（每个元素为一个字典）
    """
    try:
        if not pd.io.common.file_exists(file_path):
            print(f"导入失败：文件不存在 - {file_path}")
            return []

        df = pd.read_excel(file_path, engine='openpyxl')
        if df.empty:
            print(f"导入警告：文件为空 - {file_path}")
            return []

        return df.to_dict('records')
    except FileNotFoundError:
        print(f"导入失败：文件未找到 - {file_path}")
        return []
    except PermissionError:
        print(f"导入失败：没有权限读取文件 - {file_path}")
        return []
    except Exception as e:
        print(f"导入Excel失败: {str(e)}")
        return []


def validate_excel_file(file_path: str) -> bool:
    """
    验证Excel文件是否存在且可读
    :param file_path: Excel文件路径
    :return: 文件是否有效
    """
    try:
        if not pd.io.common.file_exists(file_path):
            print(f"验证失败：文件不存在 - {file_path}")
            return False

        pd.read_excel(file_path, engine='openpyxl', nrows=0)  # 尝试读取文件头
        return True
    except Exception as e:
        print(f"验证失败：文件无法读取 - {str(e)}")
        return False

def export_excel_to_bytes(data: List[Dict]) -> BytesIO:
    """导出数据到Excel字节流"""
    try:
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return output
    except Exception as e:
        print(f"导出Excel字节流失败: {str(e)}")
        return BytesIO()