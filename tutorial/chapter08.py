# -*- coding: utf-8 -*-
import time

from fastapi import APIRouter, BackgroundTasks

app08 = APIRouter()


def task():
    time.sleep(10)
    print('task done.')


@app08.get('/preGroundTask')
def pre_ground_task():
    task()
    return {'result': 'ok'}


# 实现类似 Celery 的后台任务
@app08.get('/backGroundTask')
def back_ground_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(func=task)
    return {'result': 'ok'}
