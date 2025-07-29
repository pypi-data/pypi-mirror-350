from fastpluggy.core.config import BaseDatabaseSettings


class ScheduledQuerySettings(BaseDatabaseSettings):
    notification_on_run: bool = False
    interval: int = 30
    prometheus_enabled: bool = True
