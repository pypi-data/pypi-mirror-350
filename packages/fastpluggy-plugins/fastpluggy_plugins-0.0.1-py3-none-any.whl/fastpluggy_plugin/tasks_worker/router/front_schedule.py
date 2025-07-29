import json

from fastapi import Request, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from fastpluggy_plugin.crud_tools.crud_link_helper import CrudLinkHelper
from fastpluggy_plugin.crud_tools.schema import CrudAction
from fastpluggy.core.database import get_db
from fastpluggy.core.dependency import get_view_builder
from fastpluggy.core.flash import FlashMessage
from fastpluggy.core.tools.fastapi import redirect_to_previous
from fastpluggy.core.view_builer.components.button import AutoLinkView
from fastpluggy.core.view_builer.components.list import ListButtonView
from fastpluggy.core.view_builer.components.render_field_tools import RenderFieldTools
from fastpluggy.core.view_builer.components.table_model import TableModelView
from .tools.task_form import TaskFormView
from ..config import TasksRunnerSettings
from ..models.scheduled import ScheduledTaskDB
from ..schema.request_input import CreateScheduledTaskRequest

front_schedule_task_router = APIRouter(
    tags=["task_router"],
)


@front_schedule_task_router.get("/scheduled_tasks/", name="list_scheduled_tasks")
def list_scheduled_tasks(request: Request,
                         view_builder=Depends(get_view_builder)):
    buttons = []
    settings = TasksRunnerSettings()
    if settings.allow_create_schedule_task:
        buttons.append(AutoLinkView(label="Create a Scheduled Task", route_name='create_scheduled_task', ))
    items = [
        ListButtonView(
            buttons=buttons
        ),
        TableModelView(
            model=ScheduledTaskDB,
            title="Task scheduled",
            links=[
                AutoLinkView(
                    label="View Last Task",
                    route_name="task_details",  # from your existing router
                    param_inputs={"task_id": '<last_task_id>'},
                    condition=lambda row: row['last_task_id'] is not None
                ),
                # TODO : add a retry button
                CrudLinkHelper.get_crud_link(model=ScheduledTaskDB, action=CrudAction.EDIT),
            ],
            field_callbacks={
                ScheduledTaskDB.enabled: RenderFieldTools.render_boolean,
                # ScheduledTaskDB.last_status: RenderFieldTools.render_enum,
            },
            exclude_fields=[
                ScheduledTaskDB.created_at,
                ScheduledTaskDB.updated_at,
                ScheduledTaskDB.kwargs,
                ScheduledTaskDB.notify_on
            ]
        )
    ]

    return view_builder.generate(
        request,
        title="List of scheduled tasks",
        items=items
    )


@front_schedule_task_router.get("/create_scheduled_task", name="create_scheduled_task")
def create_scheduled_task(
        request: Request,
        view_builder=Depends(get_view_builder)
):
    view = TaskFormView(
        title="New Scheduled Task",
        submit_url=str(request.url_for("create_scheduled_task_post")),
        url_after_submit=str(request.url_for("list_scheduled_tasks")),
        mode="schedule_task",
    )
    return view_builder.generate(request, [view])


@front_schedule_task_router.post("/create_scheduled_task", name="create_scheduled_task_post")
def create_scheduled_task_post(
        request: Request,
        payload: CreateScheduledTaskRequest,
        method: str = 'web',
        db: Session = Depends(get_db)
):
    task = ScheduledTaskDB(
        name=payload.name,
        function=payload.function,
        cron=payload.cron,
        interval=payload.interval,
        kwargs=json.dumps(payload.kwargs),
        notify_on=json.dumps(payload.notify_on),
        enabled=True,
    )
    db.add(task)
    db.commit()
    mesg = FlashMessage.add(request=request, message=f"Scheduled Task {payload.name} created !")

    if method == "web":
        return redirect_to_previous(request)
    else:
        return JSONResponse(content=mesg.to_dict())
