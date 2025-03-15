import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loyalty_project.settings')

app = Celery('loyalty_project')

# Load any custom configuration from Django settings, using the CELERY namespace.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed apps.
app.autodiscover_tasks()

# Optional: A simple debug task to test Celery.
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
