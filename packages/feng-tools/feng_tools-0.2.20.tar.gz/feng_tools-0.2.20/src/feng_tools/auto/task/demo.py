# 初始化数据库
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from feng_tools.auto.task.task_manager import TaskManager
from feng_tools.orm.sqlalchemy.init import Base


def init_db(db_url='sqlite:///task_manager.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


if __name__ == '__main__':
    # 初始化任务管理器
    manager = TaskManager(max_concurrent_tasks=4)

    # 添加命令行任务
    manager.add_task(
        name="Daily Backup",
        task_type="command",
        command="pg_dump mydb > backup.sql",
        schedule="0 2 * * *"  # 每天凌晨2点
    )

    # 添加Python函数任务
    manager.add_task(
        name="Process Data",
        task_type="python_function",
        command="my_project.data_processor.process_data",
        schedule="every 30 minutes",
        args=[1, 2, 3],
        kwargs={"option": "fast"}
    )

    # 添加立即执行的测试任务
    manager.add_task(
        name="Test Task",
        task_type="command",
        command="echo 'Hello World'",
        schedule="immediate"
    )

    try:
        # 主线程保持运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.shutdown()