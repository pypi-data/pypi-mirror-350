# _*_coding:utf-8 _*_
# Author: df_coding
# Time: 2025/4/22 下午1:49

"""
基本任务
"""

from celery import Task


class BaseTask(Task):
    def __init__(self):
        pass

    def before_start(self, task_id, args, kwargs):
        """Handler called before the task starts.

        Arguments:
            task_id (str): Unique id of the task to execute.
            args (Tuple): Original arguments for the task to execute.
            kwargs (Dict): Original keyword arguments for the task to execute.

        Returns:
            None: The return value of this handler is ignored.
        """
        # 版本不一致导致取值为空的解决方法
        periodic_task_name = self.request.properties.get('periodic_task_name')
        if periodic_task_name:
            self.request.periodic_task_name = periodic_task_name

        self.backend.mark_as_started(task_id=task_id)  # 显式标记任务开始

    def on_success(self, retval, task_id, args, kwargs):
        """

        :param retval:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        # print(self.name)
        # print(self.request.hostname)
        # print(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, exc_info):
        """

        :param exc:
        :param task_id:
        :param args:
        :param kwargs:
        :param exc_info:
        :return:
        """
        print('{0!r} failed: {1!r}'.format(task_id, exc))
