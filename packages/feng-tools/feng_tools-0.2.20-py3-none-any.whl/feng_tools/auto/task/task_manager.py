import importlib
import json
import logging
import os
import subprocess
import time
import traceback
from datetime import datetime
from functools import partial
from multiprocessing import Pool, cpu_count
from threading import Thread

import schedule
from sqlalchemy.orm import Session

from feng_tools.auto.task.task_models import TaskExecution, ScheduledTask


class TaskManager:
    def __init__(self, db_session:type[Session], max_concurrent_tasks=None, log_dir='logs'):
        self.max_concurrent_tasks = max_concurrent_tasks or cpu_count()
        self.log_dir = os.path.abspath(log_dir)
        self.current_running_tasks = 0
        self.process_pool = Pool(processes=self.max_concurrent_tasks)
        self.Session = db_session

        # 初始化日志
        os.makedirs(self.log_dir, exist_ok=True)
        self.setup_logging()

        # 启动后台任务检查线程
        self._running = True
        self.monitor_thread = Thread(target=self._monitor_tasks, daemon=True)
        self.monitor_thread.start()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(self.log_dir, 'task_manager.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('TaskManager')

    def add_task(self, name, task_type, command, schedule_expr, args=None, kwargs=None, enabled=True):
        """添加新任务"""
        session = self.Session()

        task = ScheduledTask(
            name=name,
            task_type=task_type,
            command=command,
            schedule=schedule_expr,
            args=json.dumps(args) if args else None,
            kwargs=json.dumps(kwargs) if kwargs else None,
            enabled=enabled
        )

        session.add(task)
        session.commit()
        session.close()
        self.logger.info(f'Added new task: {name}')

        # 如果是立即执行的任务，加入队列
        if schedule_expr == 'immediate' and enabled:
            self._execute_task(task.id)

    def _monitor_tasks(self):
        """后台线程检查未完成任务和定时任务"""
        while self._running:
            try:
                # 检查未完成的执行
                self._check_pending_tasks()

                # 检查定时任务
                self._check_scheduled_tasks()

                # 运行计划任务
                schedule.run_pending()

                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Monitor thread error: {str(e)}")
                time.sleep(5)

    def _check_pending_tasks(self):
        """检查未完成的任务"""
        session = self.Session()
        try:
            pending_tasks = session.query(ScheduledTask).filter(
                ScheduledTask.enabled == True,
                ~ScheduledTask.executions.any(TaskExecution.status.in_(['running', 'success']))
                # 这里可以根据需要添加更复杂的查询条件
            ).all()

            for task in pending_tasks:
                if self.current_running_tasks < self.max_concurrent_tasks:
                    self._execute_task(task.id)
        finally:
            session.close()

    def _check_scheduled_tasks(self):
        """设置定时任务"""
        session = self.Session()
        try:
            tasks = session.query(ScheduledTask).filter(
                ScheduledTask.enabled == True
            ).all()

            # 清除所有现有计划
            schedule.clear()

            for task in tasks:
                if task.schedule.startswith('every '):
                    # 处理时间间隔任务，如 "every 10 minutes"
                    self._setup_interval_task(task)
                elif ' ' in task.schedule.strip():
                    # 处理cron表达式
                    self._setup_cron_task(task)
        finally:
            session.close()

    def _setup_interval_task(self, task):
        """设置间隔任务"""
        try:
            parts = task.schedule.split()
            interval = int(parts[1])
            unit = parts[2].rstrip('s')  # 移除可能存在的复数's'

            job_func = partial(self._execute_task, task.id)

            if unit == 'second':
                schedule.every(interval).seconds.do(job_func)
            elif unit == 'minute':
                schedule.every(interval).minutes.do(job_func)
            elif unit == 'hour':
                schedule.every(interval).hours.do(job_func)
            else:
                self.logger.warning(f"Unsupported interval unit: {unit} for task {task.id}")
        except Exception as e:
            self.logger.error(f"Error setting up interval task {task.id}: {str(e)}")

    def _setup_cron_task(self, task):
        """设置cron任务"""
        try:
            from croniter import croniter
            # 验证cron表达式
            croniter(task.schedule)

            job_func = partial(self._execute_task, task.id)
            schedule.every().day.at("00:00").do(
                lambda: schedule.every().hour.do(job_func) if task.schedule == "0 * * * *" else job_func()
            )
            # 这里简化了cron表达式的处理，实际应用中可能需要更复杂的转换
        except ImportError:
            self.logger.warning("croniter package not installed, cron tasks won't work")
        except Exception as e:
            self.logger.error(f"Error setting up cron task {task.id}: {str(e)}")

    def _execute_task(self, task_id):
        """执行任务"""
        if self.current_running_tasks >= self.max_concurrent_tasks:
            self.logger.warning(f"Max concurrent tasks reached, skipping task {task_id}")
            return

        self.current_running_tasks += 1
        self.process_pool.apply_async(
            self._execute_task_sync,
            (task_id,),
            callback=lambda _: self._task_completed(),
            error_callback=lambda e: self._task_completed(error=e)
        )

    def _task_completed(self, error=None):
        """任务完成回调"""
        self.current_running_tasks -= 1
        if error:
            self.logger.error(f"Task completed with error: {str(error)}")

    def _execute_task_sync(self, task_id):
        """同步执行任务"""
        session = self.Session()
        try:
            task = session.query(ScheduledTask).get(task_id)
            if not task or not task.enabled:
                return

            # 创建执行记录
            execution = TaskExecution(
                task_id=task.id,
                start_time=datetime.now(),
                status='running',
                pid=os.getpid()
            )
            session.add(execution)
            session.commit()

            # 准备日志文件
            log_filename = f'task_{task.id}_exec_{execution.id}.log'
            log_path = os.path.join(self.log_dir, log_filename)
            execution.log_path = log_path
            session.commit()

            # 配置任务日志
            task_logger = logging.getLogger(f'Task_{task.id}')
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            task_logger.addHandler(file_handler)

            try:
                args = json.loads(task.args) if task.args else []
                kwargs = json.loads(task.kwargs) if task.kwargs else {}

                if task.task_type == 'command':
                    # 执行命令行任务
                    result = subprocess.run(
                        task.command,
                        shell=True,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        timeout=task.timeout if task.timeout else None,
                        cwd=os.getcwd()  # 在当前工作目录执行
                    )
                    output = result.stdout.decode()
                    return_code = result.returncode

                elif task.task_type == 'python_function':
                    # 执行Python函数任务
                    module_path, func_name = task.command.rsplit('.', 1)
                    module = importlib.import_module(module_path)
                    func = getattr(module, func_name)

                    # 在当前Python环境中执行
                    output = func(*args, **kwargs)
                    return_code = 0

                    if not isinstance(output, str):
                        output = str(output)

                else:
                    raise ValueError(f"Unknown task type: {task.task_type}")

                # 更新执行结果为成功
                execution.status = 'success'
                execution.return_code = return_code
                execution.output = output
                execution.end_time = datetime.now()
                session.commit()

                task_logger.info(f"Task {task.name} executed successfully")
                task_logger.info(f"Output:\n{output}")

            except Exception as e:
                # 处理任务执行失败
                error_msg = traceback.format_exc()
                execution.status = 'failed'
                execution.output = error_msg
                execution.end_time = datetime.now()
                session.commit()

                task_logger.error(f"Task {task.name} failed")
                task_logger.error(error_msg)

                # 重试逻辑可以在这里实现

        finally:
            session.close()
            if 'task_logger' in locals():
                task_logger.removeHandler(file_handler)
                file_handler.close()

    def shutdown(self):
        """关闭任务管理器"""
        self._running = False
        self.process_pool.close()
        self.process_pool.join()
        self.monitor_thread.join()
        self.logger.info("Task manager shutdown complete")