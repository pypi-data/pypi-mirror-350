# -*- coding: utf-8 -*-

from celery_worker.app import app, logger
from celery_worker.tasks.base import BaseTask


@app.task(bind=True, base=BaseTask)
def add(self, n, m):
    try:
        logger.info(self.request.id)
        logger.info(f'{n} + {m}的结果：{n + m}')
    except Exception as e:
        print(e.args)

    return n + m
