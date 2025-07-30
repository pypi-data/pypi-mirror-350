import asyncio
import json
import logging
import datetime
from datetime import timezone, timedelta
from typing import Annotated

from croniter import croniter
from fastpluggy.core.database import session_scope
from fastpluggy.core.tools.inspect_tools import InjectDependency
from fastpluggy.fastpluggy import FastPluggy
from loguru import logger
from sqlalchemy import or_

from ..models.scheduled import ScheduledTaskDB
from ..task_registry import task_registry


@task_registry.register(name="schedule_loop", allow_concurrent=False)
async def schedule_loop(fast_pluggy: Annotated[FastPluggy, InjectDependency]):
    from ..config import TasksRunnerSettings

    logging.info("[SCHEDULER] Started schedule loop")
    settings = TasksRunnerSettings()

    while settings.scheduler_enabled:
        logging.debug("[SCHEDULER] Schedule loop running")

        if not fast_pluggy.get_global('tasks_worker').executor.is_running():
            logging.debug("[SCHEDULER] Executor not running -> exit scheduler")
            break

        now = datetime.datetime.now(timezone.utc)

        try:
            with session_scope() as db:
                tasks = db.query(ScheduledTaskDB).filter(
                    ScheduledTaskDB.enabled == True,
                    or_(
                        ScheduledTaskDB.next_run <= now,
                        ScheduledTaskDB.next_run == None
                    )
                ).all()

                if not tasks:
                    logger.info("No scheduled tasks found")

                for sched in tasks:
                    try:
                        sched.last_attempt = datetime.datetime.now(datetime.UTC)
                        db.add(sched)
                        db.commit()

                        func = task_registry.get(sched.function)
                        if not func:
                            logger.warning(f"[SCHEDULER] Function not found: {sched.function}")
                            db.add(sched)
                            db.commit()
                            continue

                        logger.info(f"[SCHEDULER] Triggering task: {sched.name}")

                        # Parse kwargs
                        try:
                            kwargs = json.loads(sched.kwargs or "{}")
                        except Exception as e:
                            logger.exception(f"[SCHEDULER] Failed to parse kwargs: {e}")
                            db.add(sched)
                            db.commit()
                            continue

                        # Submit task and store its ID
                        task_id = FastPluggy.get_global('tasks_worker').submit(
                            func,
                            task_name=sched.name,
                            notify_config=json.loads(sched.notify_on or "[]"),
                            task_origin="scheduler",
                            kwargs=kwargs,
                        )
                        sched.last_task_id = task_id

                        # Compute next run
                        if sched.cron:
                            sched.next_run = croniter(sched.cron, now).get_next(datetime.datetime)
                        elif sched.interval:
                            sched.next_run = sched.last_attempt + timedelta(minutes=float(sched.interval))
                        db.add(sched)
                        db.commit()

                    except Exception as task_error:
                        logger.exception(f"[SCHEDULER] Error scheduling task '{sched.name}': {task_error}")
                        db.rollback()

        except Exception as e:
            logger.exception(f"[SCHEDULER] Error in main scheduling loop: {e}")

        await asyncio.sleep(settings.scheduler_frequency)
