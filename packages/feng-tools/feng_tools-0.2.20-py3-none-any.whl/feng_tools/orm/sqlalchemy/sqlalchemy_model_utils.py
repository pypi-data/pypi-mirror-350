"""
sqlalchemy 的模型工具
"""
import json
from typing import Type

from feng_tools.file.json.json_encoder import JsonEncoder
from feng_tools.orm.sqlalchemy.base_models import Model


def to_dict(model):
    """Model实例转dict"""
    model_dict = dict(model.__dict__)
    del model_dict['_sa_instance_state']
    return model_dict


def to_dict2(model):
    """单个对象转dict(效果等同上面的那个)"""
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


def to_json(model) -> str:
    """model或model集合转换为json字符串"""
    if isinstance(model, list):
        return json.dumps([to_dict2(tmp) for tmp in model], cls=JsonEncoder, indent=4, ensure_ascii=False)
    else:
        return json.dumps(to_dict(model), cls=JsonEncoder, indent=4, ensure_ascii=False)


def list_to_dictlist(model_list):
    """多个对象转dict"""
    return [to_dict2(tmp) for tmp in model_list]


def list_to_json(model_list):
    """多个对象转json字符串"""
    return json.dumps([to_dict2(tmp) for tmp in model_list], cls=JsonEncoder, indent=4, ensure_ascii=False)


def copy_model(model):
    """复制模型，示例如下：
        info = GroupInfo(name='test')
        info_bak = model_utils.copy_model(info)
    """
    return type(model)(**to_dict(model))


def copy_model_data(old_model, new_model_class: Type[Model]):
    """
    复制Model数据
    :param old_model: 源model对象
    :param new_model_class: 目标Model类
    :return: 目标model对象
    """
    old_model_dict = to_dict(old_model)
    params_set = {c.name for c in new_model_class.__table__.columns}
    new_model_dict = {tmp_key: tmp_value for tmp_key, tmp_value in old_model_dict.items() if tmp_key in params_set}
    return new_model_class(**new_model_dict)



def is_model_class(model_class: type) -> bool:
    """是否是Model的子类"""
    if model_class:
        return '__table__' in model_class.__dict__
    return False


def is_model_instance(model_instance) -> bool:
    """是否是Model的实例"""
    if model_instance and not isinstance(model_instance, str) and not isinstance(model_instance, int) and not isinstance(model_instance, float) and not isinstance(model_instance, tuple) and not isinstance(model_instance, list) and not isinstance(model_instance, dict):
        return '_sa_instance_state' in model_instance.__dict__
    return False

def copy_new_model_to_db_model(db_model, new_model: Model):
    """将新实例的属性值拷贝到数据库实例"""
    for key, value in new_model.__dict__.items():
        if not key.startswith('_') and key != 'id' and hasattr(db_model, key):
            setattr(db_model, key, value)
    return db_model