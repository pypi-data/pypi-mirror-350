import traceback

from sqlalchemy import select, func, Sequence
from sqlalchemy.orm import Session
from sqlalchemy.sql.ddl import DropSequence, CreateSequence

from feng_tools.orm.sqlalchemy.sqlalchemy_session_tools import SqlalchemySessionTool


class SequenceTool:
    def __init__(self, session_tool:SqlalchemySessionTool):
        self.session_tool = session_tool

    def create_sequence(self, sequence_name: str):
        with self.session_tool.session_maker() as db:
            try:
                # create sequence {sequence_name} start with 1 increment by 1 nocache nocycle
                db.execute(CreateSequence(Sequence(name=sequence_name, start=1, increment=1, cycle=False, cache=False),
                                          if_not_exists=True))
                db.commit()
            except Exception as e:
                db.rollback()
                traceback.print_exc()
                raise e


    def drop_sequence(self, sequence_name: str):
        with self.session_tool.session_maker() as db:
            try:
                db.execute(DropSequence(Sequence(sequence_name)))
                db.commit()
            except Exception as e:
                db.rollback()
                traceback.print_exc()
                raise e
    def get_sequence_next_value(self, sequence_name: str, db: Session = None) -> int:
        """获取序列的下一个值"""
        if db:
            result = db.execute(select(func.next_value(Sequence(sequence_name))))
            return result.first()[0]
        with self.session_tool.session_maker() as db:
            result = db.execute(select(func.next_value(Sequence(sequence_name))))
            return result.first()[0]


    def update_sequence_value_to(self, sequence_name: str, to_value: int):
        """
        更新序列值到某个值
        :param sequence_name: 序列名
        :param to_value: 要到的值
        :return:
        """
        with self.session_tool.session_maker() as db:
            now_value = self.get_sequence_next_value(sequence_name, db=db)
            for i in range(now_value, to_value + 1):
                result = self.get_sequence_next_value(sequence_name, db=db)
                if result == to_value:
                    break
