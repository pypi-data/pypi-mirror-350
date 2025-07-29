# plugin.py

from typing import Annotated, Any
from loguru import logger

from fastpluggy.core.module_base import FastPluggyBaseModule
from fastpluggy.core.tools.inspect_tools import InjectDependency
from fastpluggy.fastpluggy import FastPluggy

from .config import ScheduledQuerySettings


def get_scheduler_query_router():
    from .router import scheduler_query_router

    return scheduler_query_router

class ScheduledQueryPlugin(FastPluggyBaseModule):

    module_name: str = "scheduled_query"
    module_version: str = "0.1.2"

    module_menu_name: str = "Scheduled Query"
    module_menu_icon: str = "fas fa-edit"

    module_settings: Any = ScheduledQuerySettings
    module_router: Any = get_scheduler_query_router

    depends_on: dict = {
        "tasks_worker": ">=0.2.0",
    }

    def on_load_complete(self, fast_pluggy: Annotated["FastPluggy", InjectDependency]) -> None:
        logger.info("Add query runner to executor")

        from .tasks import collect_execute_scheduled_query

        task_runner = FastPluggy.get_global("tasks_worker")
        task_runner.submit(
            collect_execute_scheduled_query,
            task_name='scheduled query',
            notify_config=[],
            task_origin="module_load",
            allow_concurrent=False
        )
