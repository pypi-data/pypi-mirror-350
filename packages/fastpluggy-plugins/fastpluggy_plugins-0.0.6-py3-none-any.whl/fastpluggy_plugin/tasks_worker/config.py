from typing import Optional, List

from fastpluggy.core.config import BaseDatabaseSettings


class TasksRunnerSettings(BaseDatabaseSettings):

    # Thread pool settings
    thread_pool_max_workers: Optional[int] = None  # None means use default (CPU count * 5)

    # Scheduler
    scheduler_enabled: bool = True
    scheduler_frequency: float = 5
    allow_create_schedule_task: bool = True

    # notifier
    external_notification_loaders: Optional[List[str]] = []

    # Registry/Discover of tasks
    enable_auto_task_discovery: bool = True  # 🔍 Enables scanning for task functions
    # Celery
    discover_celery_tasks: bool = True
    celery_app_path: str = "myproject.worker:celery_app"  # Path to the Celery app object

    store_task_db: bool = True
    #store_task_notif_db: bool = False

    # Purge
    purge_enabled :bool = True
    purge_after_days: int = 30

# maybe add a module prefix
#    class Config:
#        env_prefix = "tasks_worker_"
    watchdog_enabled: bool = True
    #watchdog_frequency: float = 5
    watchdog_timeout_minutes: int = 120

    # WARN: if you enable this, you need to ensure you using a process pool and not a thread
    #       in some cases, the GitPython seems to never finish and let the future running into pool stuck forever,
    #       and we are not able to restart it correctly and can't accept new jobs
    #       Maybe a fix can be done like https://chatgpt.com/c/682e5fd2-9340-8009-8960-d8cda40f3f2e
    auto_update_plugins: bool = False
