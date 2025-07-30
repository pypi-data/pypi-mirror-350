from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from feng_tools.orm.sqlalchemy.init import Base


class ScheduledTask(Base):
    __tablename__ = 'scheduled_tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    task_type = Column(String(20), nullable=False)  # 'command' or 'python_function'
    command = Column(Text, nullable=False)  # 命令行或函数路径
    schedule = Column(String(100), nullable=False)  # cron表达式或时间间隔
    args = Column(Text)  # JSON格式的参数
    kwargs = Column(Text)  # JSON格式的关键字参数
    max_retries = Column(Integer, default=3)
    timeout = Column(Integer)  # 超时时间(秒)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    executions = relationship("TaskExecution", back_populates="task")


class TaskExecution(Base):
    __tablename__ = 'scheduled_task_executions'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('scheduled_tasks.id'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(String(20), nullable=False)  # pending, running, success, failed
    return_code = Column(Integer)
    output = Column(Text)
    log_path = Column(String(255))
    pid = Column(Integer)

    task = relationship("ScheduledTask", back_populates="executions")


