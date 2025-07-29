import logging
import signal
import traceback
import uuid
from datetime import datetime, UTC
from time import sleep
from typing import Optional, List, Tuple

from fastpluggy.core.database import session_scope
from fastpluggy.core.tools.inspect_tools import call_with_injection
from fastpluggy.fastpluggy import FastPluggy
from .repository.report import init_report_from_context, save_report, update_report
from .config import TasksRunnerSettings
from .executor.thread_executor import InstrumentedThreadPoolExecutor
from .log_handler import log_handler_context
from .models.context import TaskContextDB
from .models.report import TaskReportDB
from .notifiers.registry import resolve_notifiers_for_task
from .repository.context import save_context
from .schema.context import TaskContext
from .schema.notifier import NotifierConfig
from .schema.report import TaskReport
from .schema.status import TaskStatus
from .services.lock_manager import TaskLockManager
from .services.notification_service import TaskNotificationService


class TaskRunner:
    def __init__(self, fast_pluggy: FastPluggy):
        """
        Initialize a new TaskRunner instance.
        """

        self.fast_pluggy = fast_pluggy

        self.worker_id = str(uuid.uuid4())
        self.lock_manager = TaskLockManager(worker_id=self.worker_id)
        self.settings = TasksRunnerSettings()

        self.executor = InstrumentedThreadPoolExecutor(max_workers=self.settings.thread_pool_max_workers)

        # Register graceful shutdown on SIGINT and SIGTERM
        signal.signal(signal.SIGINT, self.executor.graceful_shutdown)
        signal.signal(signal.SIGTERM, self.executor.graceful_shutdown)

    def submit(
            self,
            func,
            args: Optional[Tuple] = None,
            kwargs: Optional[dict] = None,
            task_name: Optional[str] = None,
            notify_config: Optional[List[NotifierConfig]] = None,
            max_retries: int = 0,
            retry_delay: int = 0,
            parent_task_id: Optional[str] = None,
            task_origin: str = "unk",
            allow_concurrent: Optional[bool] = None,
    ) -> Optional[str]:
        """
        Register and submit a new task for execution.
        If a task is not allowed to run concurrently and an instance is already running, it returns None.
        """
        task_id = str(uuid.uuid4())
        task_name = task_name or func.__name__

        # Enforce concurrency rules with a lock.
        if allow_concurrent is None:
            allow_concurrent = self.it_allow_concurrent(func)

        context = TaskContext(
            task_id=task_id,
            task_name=task_name,
            func_name=func.__name__,
            args=list(args or ()),
            kwargs=kwargs or {},
            notifier_config=notify_config or [],
            parent_task_id=parent_task_id,
            max_retries=max_retries,
            retry_delay=retry_delay,
            task_origin=task_origin,
            allow_concurrent=allow_concurrent,
        )
        context.notifiers = resolve_notifiers_for_task(context=context)

        if self.settings.store_task_db:
            save_context(context)

        if not allow_concurrent:
            if not self.lock_manager.acquire_lock(task_name=task_name, task_id=task_id):
                logging.info(f"[LOCK] Skipping task {task_name}, already running.")
                if self.settings.store_task_db:
                    self._record_skipped_task_report(context)
                return None

        def wrapped():
            try:
                return self.run(func, context)
            except Exception as e:
                logging.error(f"Error running task {task_id}: {e}\n{traceback.format_exc()}")
                raise
            finally:
                if not self.it_allow_concurrent(func):
                    self.lock_manager.release_lock(task_id)

        self.executor.submit_task(task_id, wrapped)
        return task_id

    def run(self, func, context: TaskContext):
        """
        Execute the task function using the provided context, managing retries and logging.
        Notifies start and end events and then prints the final report.
        """
        try:
            report = init_report_from_context(context)
            if self.settings.store_task_db:
                save_report(report)

            TaskNotificationService.notify_task_status(report, context)
            # Set up the logging handler using the context
            with log_handler_context(context) as handler:
                context.thread_handler = handler

                # Execute the task with retries using our context object
                self.run_with_retries_using_context(func, context=context, report=report)

            TaskNotificationService.notify_task_status(report, context)

            report.print()
        finally:
            TaskNotificationService.cleanup_notifiers(context)


    def run_with_retries_using_context(self, func, context: TaskContext, report: TaskReport, ) -> TaskReport:
        """
        Run a task with a given number of retries and update the report accordingly.
        """
        result = None
        tracebacks = []

        while context.max_retries == -1 or report.attempts <= context.max_retries:
            report.attempts += 1
            try:
                context_dict = {
                    FastPluggy: self.fast_pluggy,
                    TaskContext: context,
                }

                report.result = call_with_injection(
                    func,
                    context_dict=context_dict,
                    user_kwargs={**dict(zip(func.__code__.co_varnames, context.args)), **context.kwargs}
                )

                report.success = True
                break
            except Exception as err:
                logging.error(f"[TASKS_RUNNER] Task {context.task_id} failed with error: {err}")
                report.tracebacks.append(traceback.format_exc())
                if report.attempts <= context.max_retries and context.retry_delay > 0:
                    sleep(context.retry_delay)

        report.logs = context.thread_handler.get_stream_value()
        report.end_time = datetime.now(UTC)
        report.status = TaskStatus.SUCCESS if report.success else TaskStatus.FAILED
        report.error = tracebacks[-1] if tracebacks else None
        # Update the report in the DB
        if self.settings.store_task_db:
            update_report(report)
                     #     end_time=end_time,
                   #       duration=duration,
                   #       logs=logs,
                    #      result=str(result) if result is not None else None,
                      #tracebacks=tracebacks,
                     #     attempts=report.attempts,
                        #  finished=True,
                  #        finished_at=end_time,
                       #   status=TaskStatus.SUCCESS if report.success else TaskStatus.FAILED,

        return report

    def cancel_task_with_notification(self, task_id: str, db: Optional = None) -> bool:
        """
        Cancel a running task by task_id, update its status to 'manual_cancel',
        and emit a manual cancellation event.
        If no DB session is provided, a new one is obtained.
        """
        # Cancel using the Future mechanism.
        canceled_successfully = self.executor.cancel_task(task_id)
        if not canceled_successfully:
            logging.warning(f"[TASKS_RUNNER] Failed to cancel task {task_id}.")
            return False

        if self.settings.store_task_db:
            with session_scope() as db:
                # Update the task report status to 'manual_cancel'
                report = db.query(TaskReportDB).filter(TaskReportDB.task_id == task_id).first()
                if report:
                    report.status = TaskStatus.MANUAL_CANCELLED
                    db.commit()

                # Retrieve the task context to construct a TaskContext instance.
                context_db = db.query(TaskContextDB).filter(TaskContextDB.task_id == task_id).first()
                if context_db:
                    raise Exception(f"[TASKS_RUNNER] TaskContextDB for task {task_id} not found.")
                    # context = TaskContext(
                    #     task_id=context_db.task_id,
                    #     task_name=context_db.task_name,
                    #     func_name=context_db.func_name,
                    #     args=[],  # Deserialize context_db.args as needed.
                    #     kwargs={},  # Deserialize context_db.kwargs as needed.
                    # )
                else:
                    context = TaskContext(task_id=task_id, task_name="Unknown", func_name="Unknown", args=[], kwargs={})

            # Emit a manual cancellation event.
            TaskNotificationService.notify_task_status(report, context)

        return True

    def get_task_status(self, task_id: str) -> str:
        """
        Return the status of a task based on its Future state.
        Todo: unify with TaskStatus enum.
        """
        return self.executor.get_task_status(task_id)

    def get_all_active_tasks(self) -> List[Tuple[str, str]]:
        """
        Return a list of tuples (task_id, status) for all running tasks.
        """
        return self.executor.get_all_active_tasks()

    def it_allow_concurrent(self, func) -> bool:
        """
        Return True if the task function allows concurrent execution.
        """
        meta = getattr(func, "_task_metadata", {})
        return meta.get("allow_concurrent", True)

    def _record_skipped_task_report(self, context: TaskContext):
        """
        Store a task report for a task skipped due to concurrency lock.
        """
        # Initialize report with RUNNING status and DB entry
        report = init_report_from_context(context)
        report.status = TaskStatus.SKIPPED
        report.finished = True
        report.finished_at = datetime.utcnow()
        report.logs = "⛔ Task skipped due to concurrency lock.",
        report.end_time = datetime.utcnow()

        if self.settings.store_task_db:
            update_report(report)

        # Notify skip as task end
        TaskNotificationService.notify_task_status(report, context)
