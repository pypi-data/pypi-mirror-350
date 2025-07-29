from .celery_app import app

@app.task(name='fake_celery_app.tasks.add')
def add(x: int, y: int) -> int:
    """Simple add task for discovery tests."""
    return x + y

@app.task(name='fake_celery_app.tasks.mul')
def mul(x, y):
    """Simple multiply task for discovery tests."""
    return x * y

@app.task(name='fake_celery_app.tasks.echo')
def echo(message: str) -> str:
    """Echo the provided message."""
    return message
