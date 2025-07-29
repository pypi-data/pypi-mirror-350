"""
JSON工具
"""
import json
from typing import Any, Union

import pydantic_core

from feng_tools.file.json.json_encoder import JsonEncoder


def to_json(obj_data) -> str:
    """将Python中的对象转换为JSON中的字符串对象"""
    return json.dumps(obj_data, cls=JsonEncoder, ensure_ascii=False, indent=4)


def to_json_str(obj_data) -> str:
    """将Python中的对象转换为JSON中的字符串对象"""
    return json.dumps(obj_data, indent=4, ensure_ascii=False, default=pydantic_core.to_jsonable_python)


def to_obj(str_data):
    """将JSON中的字符串对象转换为Python中的对象"""
    return json.loads(str_data)


def model_to_dict(model):
    """Model实例转dict"""
    model_dict = dict(model.__dict__)
    del model_dict['_sa_instance_state']
    return model_dict


def model_to_dict2(model):
    """单个对象转dict(效果等同上面的那个)"""
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


def model_to_json(model) -> str:
    """model或model集合转换为json字符串"""
    if isinstance(model, list):
        return to_json([model_to_dict2(tmp) for tmp in model])
    else:
        return to_json(model_to_dict(model))

def read_json(file_path: str) -> dict:
    """
    读取JSON文件
    :param file_path: JSON文件路径
    :return: 解析后的字典对象
    :raises: FileNotFoundError, json.JSONDecodeError
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"文件未找到: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"JSON解析失败: {e.msg}", e.doc, e.pos)


def write_json(data: Any, file_path: str) -> bool:
    """
    写入JSON文件
    :param data: 要写入的数据
    :param file_path: JSON文件路径
    :return: 写入是否成功
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except (OSError, TypeError) as e:
        print(f"写入JSON文件失败: {str(e)}")
        return False


def pretty_print_json(data: Any) -> None:
    """
    美化打印JSON数据
    :param data: 要打印的JSON数据
    """
    try:
        print(json.dumps(data, ensure_ascii=False, indent=4))
    except (TypeError, OverflowError) as e:
        print(f"JSON美化打印失败: {str(e)}")


def is_valid_json(data: Union[str, bytes]) -> bool:
    """
    检查字符串或字节流是否为有效的JSON
    :param data: 待检查的字符串或字节流
    :return: 是否为有效JSON
    """
    try:
        json.loads(data)
        return True
    except (json.JSONDecodeError, TypeError):
        return False
