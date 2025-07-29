import re
import traceback
from copy import copy

from sqlalchemy import Column, Sequence
from sqlalchemy.orm import DeclarativeMeta

import logging

logger = logging.getLogger(__name__)



def is_postgresql_db(bases):
    """判断是否是postgresql数据库"""
    result_flag = False
    parents = [b for b in bases if isinstance(b, ModelMetaClass)]
    if parents:
        for tmp_parent in parents:
            super_parents = [tmp for tmp in tmp_parent.__bases__ if tmp.__name__ == 'Base']
            for tmp_super_parent in super_parents:
                if tmp_super_parent.__dict__.get('is_postgresql'):
                    return True
    return result_flag

class ModelMetaClass(DeclarativeMeta):
    """模型类的元类"""
    is_postgresql:bool = False
    def __new__(self, name, bases, attrs, **kwargs):
        self._check_class_name_(name, bases, attrs)
        if is_postgresql_db(bases):
            self.is_postgresql = True
            self._init_sequence_(name, bases, attrs)
        super_new = super().__new__
        parents = [b for b in bases if isinstance(b, ModelMetaClass)]
        if not parents:
            return super_new(self, name, bases, attrs)
        # 将类字段添加到columns中
        column_dict = dict()
        for p in parents:
            for k, v in p.__dict__.items():
                if isinstance(v, Column):
                    column_dict[k] = v
        for k, v in attrs.items():
            if isinstance(v, Column):
                column_dict[k] = v
        new_class = super_new(self, name, bases, attrs, **kwargs)
        setattr(new_class, '__column_dict__', column_dict)
        return new_class

    @classmethod
    def _init_sequence_(cls, class_name, class_bases, class_attrs):
        """初始化序列"""
        parents = [b for b in class_bases if isinstance(b, ModelMetaClass)]
        if not parents or '__tablename__' not in class_attrs or '__abstract__' in class_attrs:
            return
        if cls.is_postgresql:
            sequence_name = class_attrs["__tablename__"] + '_id_seq'
            if 'id' not in class_attrs:
                class_attrs['id'] = copy(getattr(parents[0], 'id'))
            try:
                id_column = class_attrs['id']
                id_column.default = Sequence(name=sequence_name, start=1, increment=1, cycle=False)
            except Exception as ex:
                logger.error(f'创建序列[{sequence_name}]失败, 异常信息：{ex}')
                traceback.print_exc()

    @classmethod
    def _check_class_name_(cls, class_name, class_bases, class_attrs):
        """检查类名"""
        parents = [b for b in class_bases if isinstance(b, ModelMetaClass)]
        if not parents:
            return
        if not re.match('[A-Z]', class_name):
            raise TypeError('Model类名[%s]请修改为首字母大写' % class_name)
        if '__doc__' not in class_attrs or len(class_attrs['__doc__'].strip(' \n')) == 0:
            raise TypeError('Model类[%s]中必须有文档注释，并且文档注释不能为空' % class_name)
