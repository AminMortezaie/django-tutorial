import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmos.settings')

app = Celery('cosmos')

# Load task modules froa little change in btc transactions.m all registered Django app configs.
app.autodiscover_tasks()

# Configure Celery to use Redis as the message broker.
app.conf.broker_url = 'redis://redis:6379/1'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    # Scheduler Name
    'update': {
        'task': 'update_transactions',
        # Schedule
        'schedule': 300.0
    },
    'update_bsc': {
        'task': 'update_bsc',
        # Schedule
        'schedule': 300.0
    },
}
