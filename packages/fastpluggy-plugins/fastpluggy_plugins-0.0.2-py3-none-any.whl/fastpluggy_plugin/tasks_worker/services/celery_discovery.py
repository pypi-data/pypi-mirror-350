from celery.schedules import crontab
from loguru import logger

from fastpluggy.core.database import session_scope
from ..repository.scheduled import ensure_scheduled_task_exists


class DummySender:
    def __init__(self):
        self.entries = {}

    def crontab_to_cronexpr(self, cb: crontab) -> str:
        """
        Given a celery.schedules.crontab, return a standard
        'minute hour dom month dow' cron expression.
        """
        return " ".join([
            str(cb._orig_minute),
            str(cb._orig_hour),
            str(cb._orig_day_of_month),
            str(cb._orig_month_of_year),
            str(cb._orig_day_of_week),
        ])

    def add_periodic_task(self, schedule, signature, name=None, **opts):
        # build a stable key for this entry
        key = name or signature.name

        # normalize schedule into either `cron` or `interval`
        cron_expr = None
        interval  = None

        if isinstance(schedule, crontab):
            cron_expr = self.crontab_to_cronexpr(schedule)
            schedule_repr = cron_expr
        else:
            # Celery allows a numeric interval or objects with .run_every
            if hasattr(schedule, "run_every"):
                interval = schedule.run_every
            elif isinstance(schedule, (int, float)):
                interval = schedule
            else:
                # fallback to repr for weird types
                schedule_repr = repr(schedule)

            schedule_repr = f"every {interval}s" if interval is not None else schedule_repr

        # 1) store in-memory for later inspection
        self.entries[key] = {
            "schedule": schedule_repr,
            "task_name": signature.name,
            "args":      getattr(signature, "args", ()),
            "kwargs":    getattr(signature, "kwargs", {}),
            **opts,
        }

        # 2) persist/upsert via your helper
        try:
            with session_scope() as db:
                ensure_scheduled_task_exists(
                    db           = db,
                    function     = signature.name,       # or pass the real fn if you have it
                    task_name    = key,
                    cron         = cron_expr,
                    interval     = interval,
                    kwargs       = self.entries[key]["kwargs"],
                    notify_config= None,
                    max_retries  = opts.get("max_retries", 0),
                    retry_delay  = opts.get("retry_delay", 0),
                )
                logger.debug(f"[SCHEDULER] Ensured DB entry for '{key}'")
        except Exception as e:
            logger.error(f"[SCHEDULER] Failed to persist '{key}': {e}")
        finally:
            pass
#            db.close()

