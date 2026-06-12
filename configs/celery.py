import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

app = Celery('autoria')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    broker_url='memory://',
    result_backend='cache+memory://',
    task_always_eager=True,
    task_eager_propagates=True
)

app.autodiscover_tasks()