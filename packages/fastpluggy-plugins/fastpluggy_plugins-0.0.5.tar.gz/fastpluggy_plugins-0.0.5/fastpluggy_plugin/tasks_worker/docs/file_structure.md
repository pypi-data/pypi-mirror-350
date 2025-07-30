
# Folder Structure (need to be updated)

tasks_worker/
    ├── runner/                    # Core task execution logic
    │   ├── runner.py              # TaskRunner class (minimal)
    │   ├── context.py             # TaskContext class
    │   ├── executor.py            # run_with_retries logic
    │   ├── log_handler.py         # Live logs & stream logs logic
    │   ├── notifier.py            # notify_start / notify_end
    │   └── status_tracker.py      # update_status_and_notify
    ├── models/
    │   ├── report.py              # TaskReportDB, TaskNotificationDB
    │   └── schedule.py            # ScheduledTaskDB
    ├── schema/
    │   └── report.py              # TaskReport (dataclass)
    ├── scheduler/
    │   └── scheduler.py           # Cron-compatible scheduler
    ├── notifiers/                
    │   ├── base.py                # BaseNotifier class
    │   ├── console.py             # ConsoleNotifier
    │   ├── slack.py               # SlackNotifier
    │   └── registry.py            # notifier_registry, register_notifiers
    ├── router/
    │   ├── api.py                 # JSON API (task info, launch)
    │   ├── front.py               # UI + WebSocket log stream
    │   └── __init__.py           
    ├── tasks/
    │   └── sample_tasks.py
    └── config.py
