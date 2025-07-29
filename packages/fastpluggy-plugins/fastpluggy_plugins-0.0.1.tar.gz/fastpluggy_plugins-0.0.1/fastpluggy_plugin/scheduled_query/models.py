from sqlalchemy import DateTime, Text, Boolean, JSON
from sqlalchemy.orm import mapped_column

from fastpluggy.core.database import Base


class ScheduledQuery(Base):
    __tablename__ = 'scheduled_queries'
    __table_args__ = {'extend_existing': True}

    name = mapped_column(Text, nullable=False)
    query = mapped_column(Text, nullable=False)
    last_executed = mapped_column(DateTime, default=None)
    cron_schedule = mapped_column(Text, nullable=False)  # CRON syntax
    last_result = mapped_column(Text, nullable=True)  # Last query result

    grafana_metric_config = mapped_column(
        JSON, nullable=True, default=None
    )  # Grafana metric export configuration

    enabled = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return (
            f"ScheduledQuery(id={self.id}, name={self.name},query={self.query}, "
            f"cron_schedule={self.cron_schedule}, last_executed={self.last_executed}, "
            f"last_result={self.last_result}, enabled={self.enabled}, "
            f"grafana_metric_config={self.grafana_metric_config})"
        )
