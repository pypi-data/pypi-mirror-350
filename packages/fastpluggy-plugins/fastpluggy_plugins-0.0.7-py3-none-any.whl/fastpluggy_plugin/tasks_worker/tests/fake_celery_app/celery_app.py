# celery_app.py
from celery import Celery
from celery.schedules import crontab
import logging

logger = logging.getLogger(__name__)

app = Celery(
    'fake_app',
    broker='memory://',  # In-memory broker for fast, isolated tests
    backend='rpc://'     # RPC backend for result handling
)

# Configure periodic tasks via beat_schedule
app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'fake_celery_app.tasks.add',
        'schedule': 10.0,
        'args': (2, 3),
    },
    'multiply-every-minute': {
        'task': 'fake_celery_app.tasks.mul',
        'schedule': 60.0,
        'args': (4, 5),
    },
    'daily-multiply-at-noon': {
        'task': 'fake_celery_app.tasks.mul',
        'schedule': crontab(hour=12, minute=0),
        'args': (10, 10),
    },
}

# Setup additional periodic tasks after config
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    logger.info('Setting up scheduled tasks')
    # Executes every 5 minutes
    sender.add_periodic_task(
        crontab(hour='*', minute='*/5'),
        'fake_celery_app.tasks.echo',
        args=('Hello from periodic echo',),
    )

# Autodiscover tasks in the tasks module
app.autodiscover_tasks(['fake_celery_app.tasks'])

