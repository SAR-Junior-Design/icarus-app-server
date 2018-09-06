import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icarus_backend.settings')

app = Celery('quick_publisher')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()