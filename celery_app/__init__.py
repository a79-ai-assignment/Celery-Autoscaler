from celery import Celery

app = Celery(
    'celery_app',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

app.conf.task_routes = {
    'celery_app.tasks.cpu_task': {'queue': 'cpu'},
    'celery_app.tasks.io_task': {'queue': 'io'},
}
