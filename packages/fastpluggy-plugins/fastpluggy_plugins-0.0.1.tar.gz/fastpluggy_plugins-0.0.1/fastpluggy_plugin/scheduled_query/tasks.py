import asyncio
import datetime
import time
from typing import Annotated

from loguru import logger
# Prometheus Metric Update Function
from prometheus_client import Gauge
from prometheus_client import REGISTRY
from sqlalchemy import text

from fastpluggy.core.database import get_db
from fastpluggy.core.tools.inspect_tools import InjectDependency
from fastpluggy.fastpluggy import FastPluggy
from .models import ScheduledQuery

# Prometheus Registry
prometheus_gauges = {}

prometheus_registry = REGISTRY


def is_query_safe(query: str) -> bool:
    forbidden_keywords = {"drop", "delete", "truncate", "alter"}
    return not any(keyword in query.lower() for keyword in forbidden_keywords)


def update_prometheus_metric(scheduled_query):
    """
    Updates the Prometheus metric for a scheduled query.
    Evaluates result as a Python object if it's a string.
    """
    try:
        config = scheduled_query.grafana_metric_config
        if not config:
            return

        metric_name = config.get("metric_name")
        labels = config.get("labels", {})

        # Evaluate the result if it's a string
        try:
            if isinstance(scheduled_query.last_result, str):
                result = eval(scheduled_query.last_result)  # Evaluate the string to a Python object
        except Exception as e:
            logger.warning(f"Failed to evaluate result for query {scheduled_query.id}: {e}")
            return

        # Extract the value from the result
        try:
            # Assuming the evaluated result is in a format like [{"count": 42}]
            if isinstance(result, list) and len(result) > 0 and "count" in scheduled_query.query.lower():
                value = float(result[0][0])
            else:
                logger.warning(f"Unexpected evaluated structure for result: {result}")
                return
        except (IndexError, ValueError, TypeError) as e:
            logger.warning(f"Error extracting value for metric {metric_name}: {e}")
            return

        # Create or update the Gauge metric
        if metric_name not in prometheus_registry._names_to_collectors:
            prometheus_gauges[metric_name] = Gauge(
                name=metric_name,
                documentation=f"Metric for query {scheduled_query.query}",
                registry=prometheus_registry
            )

            prometheus_gauges[metric_name].set(value)
        logger.info(f"Prometheus metric {metric_name} updated with value: {value}")

    except Exception as e:
        logger.exception(f"Failed to update Prometheus metric for query {scheduled_query.id}: {e}")


async def execute_scheduled_query(scheduled_query_id):
    """
    Task to execute a specific scheduled query by its ID and update Prometheus metrics.
    """
    db = next(get_db())

    try:
        # Retrieve the ScheduledQuery by its ID
        scheduled_query = db.query(ScheduledQuery).filter(ScheduledQuery.id == scheduled_query_id).first()

        if not scheduled_query:
            logger.warning(f"Query with ID {scheduled_query_id} not found.")
            return

        # Check if the query is safe
        if not is_query_safe(scheduled_query.query):
            logger.warning(f"Unsafe query detected for ID {scheduled_query.id}. Execution aborted.")
            scheduled_query.last_result = "Query rejected: contains forbidden keywords."
            scheduled_query.last_executed = datetime.datetime.utcnow()
            db.commit()
            return

        # Execute the SQL query
        result = db.execute(text(scheduled_query.query))
        db.commit()

        # Determine the result based on the type of query
        if scheduled_query.query.strip().lower().startswith("select"):
            result_str = str(result.fetchall())
        else:
            result_str = f"Rows affected: {result.rowcount}"

        # Update the ScheduledQuery object
        scheduled_query.last_result = result_str
        scheduled_query.last_executed = datetime.datetime.utcnow()
        db.commit()
        db.refresh(scheduled_query)
        logger.info(f"Query {scheduled_query.id} executed successfully with result: {result_str}")

    except Exception as e:
        logger.exception(f"Error executing query {scheduled_query.id}: {e}")
        scheduled_query.last_result = f"Error: {e}"
        scheduled_query.last_executed = datetime.datetime.utcnow()
        db.commit()
        logger.exception(f"Query {scheduled_query.id} failed with result: {e}")

    finally:
        db.close()


def collect_execute_scheduled_query(fast_pluggy: Annotated[FastPluggy, InjectDependency], ):
    from .config import ScheduledQuerySettings
    runner = fast_pluggy.get_global('tasks_worker')

    while runner.executor.is_running():
        db = next(get_db())
        try:
            list_query = db.query(ScheduledQuery).filter(ScheduledQuery.enabled == True).all()
            for item in list_query:

                settings = ScheduledQuerySettings()
                if settings.notification_on_run:
                    # todo: refactor this to use notifer
                    pass
                    #ws_manager.sync_broadcast(
                    #    message=WebSocketMessagePayload(message=f'Run scheduled query {item.query}')
                    #) if ws_manager else None
                logger.debug(f"Collecting execute scheduled query : {item}")
                asyncio.run(execute_scheduled_query(item.id))

                # Update Prometheus metrics
                if settings.prometheus_enabled and item.grafana_metric_config:
                    update_prometheus_metric(item)
                time.sleep(settings.interval)
        except Exception as e:
            logger.exception(f"Error executing query {item.id}: {e}")
        finally:
            db.close()
