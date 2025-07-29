from fastpluggy.core.database import Base
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text


class ScheduledTaskDB(Base):
    __tablename__ = "fp_task_schedule"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    function = Column(String(200), nullable=False)       # e.g., "sample_task"
    cron = Column(String(200), nullable=True)           # e.g., "*/5 * * * *"
    interval = Column(Integer, nullable=True, doc="Interval in minutes")
    enabled = Column(Boolean, default=True)
    next_run = Column(DateTime, nullable=True)
    kwargs = Column(Text, default="{}")             # JSON-encoded kwargs

    notify_on = Column(Text, default=None)  # JSON string like {"task_failed": ["slack_ops"]}

    # todo: maybe add
    #    max_retries: int = 0,
    #    retry_delay: int = 0,

    last_attempt = Column(DateTime, nullable=True)
    last_task_id = Column(String(200), nullable=True)
    last_status = Column(String(200), nullable=True)
