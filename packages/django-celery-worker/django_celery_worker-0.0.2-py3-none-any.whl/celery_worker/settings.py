# _*_coding:utf-8 _*_

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '********************'

# Application definition
INSTALLED_APPS = [
    'django_celery_beat',
    'django_celery_results',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'sqlite.db',
    },
}

# Broker 和 Result Backend 配置
broker_url = '*********************************'
result_backend = 'django_celery_results.backends:DatabaseBackend'
beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'  # 启用数据库调度器

# Celery 通用配置
enable_utc = True
timezone = 'Asia/Shanghai'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
