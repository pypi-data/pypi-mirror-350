from celery import shared_task


@shared_task(queue='task_queue_1')
def shared_task_celery(param):
    """Simple shared_task task for discovery tests."""
    return param

@shared_task(queue='task_queue_1')
def tigger_shared_task_celery(param):
    """Simple shared_task task for discovery tests."""
    from celery_app import app as celery_app
    celery_app.send_task('fake_celery_app.shared_task.py.shared_task_celery',
                         kwargs={'param': param}, queue='db')
    return param