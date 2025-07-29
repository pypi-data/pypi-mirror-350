# _*_coding:utf-8 _*_

import os
from celery import Celery, platforms
from celery.utils.log import get_task_logger

from celery_worker.plugin import locate_celery_config, load_tasks_dynamically

platforms.C_FORCE_ROOT = True
logger = get_task_logger(__name__)

celery_config = locate_celery_config()
# print("\nConfigName ->", celery_config)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', celery_config)

app = Celery('task')
app.config_from_object(celery_config, namespace="CELERY")

# 自动发现任务
app.autodiscover_tasks()

# 动态引入任务模块
load_tasks_dynamically(app.conf.get("task_modules", []))
