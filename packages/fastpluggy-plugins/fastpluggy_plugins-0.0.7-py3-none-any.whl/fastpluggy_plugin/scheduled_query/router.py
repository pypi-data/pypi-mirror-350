from fastapi import APIRouter, Depends, Request
from fastpluggy.core.view_builer.components.custom import CustomTemplateView
from sqlalchemy.orm import Session, selectinload

from fastpluggy.core.auth import require_authentication
from fastpluggy.core.database import get_db
from fastpluggy.core.dependency import get_view_builder
from fastpluggy.core.view_builer.components.render_field_tools import RenderFieldTools
from fastpluggy.core.view_builer.components.table_model import TableModelView
from .models import ScheduledQuery

scheduler_query_router = APIRouter(
    tags=["scheduler_query"],
    dependencies=[Depends(require_authentication)]
)


@scheduler_query_router.get("/")
def read_scheduled_queries(
        request: Request,
        db: Session = Depends(get_db),
        view_builder=Depends(get_view_builder)
):
    """
    Retrieve a list of scheduled queries.
    """
    items = [
        TableModelView(
            model=ScheduledQuery,
            fields=['id', 'name', 'query', 'last_executed', 'cron_schedule', 'enabled', 'last_result'],
            field_callbacks={
                ScheduledQuery.query: lambda query: query[:50] + '...' if query else None,
                ScheduledQuery.enabled: RenderFieldTools.render_boolean
            },
        )
    ]
    return view_builder.generate(
        request,
        items=items,
        title='Scheduled Queries',
    )

@scheduler_query_router.get("/cards")
def read_scheduled_queries(
        request: Request,
        db: Session = Depends(get_db),
        view_builder=Depends(get_view_builder)
):
    """
    Retrieve a list of scheduled queries.
    """

    all_queries = (
        db.query(ScheduledQuery).where(ScheduledQuery.enabled == True)
        .options(selectinload(ScheduledQuery.execution_history))
        .all()
    )

    widgets = []
    for q in all_queries:
        widgets.append({
            "type": "custom",
            "template": "scheduled_query/scheduled_query_card.html.j2",
            "context": {"scheduled_query": q}
        })

    items = [ CustomTemplateView(
        template_name="widgets/grid.html.j2",
        context={
            "request": request,
            "grid_title": "Scheduled Query Dashboard",
            "widgets": widgets,
        },
    )]
    return view_builder.generate(
        request,
        items=items,
        title='Scheduled Queries',
    )
