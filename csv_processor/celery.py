from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csv_processor.settings')

app = Celery('csv_processor')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Manually set broker and result backend
app.conf.broker_url = "redis://localhost:6380/0"  # Ensure Redis is running on port 6380
app.conf.result_backend = "redis://localhost:6380/0"  # Add Redis as the result backend

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    return "Task executed successfully!"
