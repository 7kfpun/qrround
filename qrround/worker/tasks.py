from celery import Celery


celery = Celery('tasks', broker='')

@celery.task
def add(x, y):
    return x + y
