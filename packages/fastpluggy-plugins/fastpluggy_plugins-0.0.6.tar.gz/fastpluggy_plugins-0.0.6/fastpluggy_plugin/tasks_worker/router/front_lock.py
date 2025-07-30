from fastapi import APIRouter, Request, Depends, HTTPException, Query
from starlette.responses import JSONResponse

from fastpluggy.core.dependency import get_view_builder
from fastpluggy.core.flash import FlashMessage
from fastpluggy.core.tools.fastapi import redirect_to_previous
from fastpluggy.core.view_builer.components.button import AutoLinkView
from fastpluggy.core.view_builer.components.list import ListButtonView
from fastpluggy.core.view_builer.components.table import TableView
from ..services.lock_manager import TaskLockManager

task_lock_router = APIRouter(tags=["task_locks"])


@task_lock_router.get("/task_locks", name="view_task_locks")
def view_task_locks(request: Request, view_builder=Depends(get_view_builder)):
    # Get all locks from the in-memory storage
    locks = TaskLockManager.get_all_locks()

    # Convert locks to a format suitable for TableView
    lock_data = [
        {
            "task_id": task_id,
            "task_name": task_name,
            "acquired_at": acquired_at,
            "locked_by": locked_by
        }
        for task_id, task_name, acquired_at, locked_by in locks
    ]

    items = [
        ListButtonView(buttons=[
            AutoLinkView(label="Back to Task Dashboard", route_name="dashboard_tasks_worker"),
        ]),
        TableView(
            title="Current Task Locks",
            data=lock_data,
            fields=["task_id", "task_name", "acquired_at", "locked_by"],
            headers={
                "task_id": "Task ID",
                "task_name": "Task Name",
                "acquired_at": "Acquired At",
                "locked_by": "Locked By"
            },
            links=[
                AutoLinkView(
                    label="Force Release",
                    route_name="force_release_task_lock",
                    param_inputs={"task_id": "<task_id>", 'method': 'web'}
                )
            ]
        )
    ]
    return view_builder.generate(request, items=items, title="Task Locks")


@task_lock_router.get("/task_locks/release", name="force_release_task_lock")
def force_release_task_lock(
        request: Request,
        task_id: str = Query(...),
        method: str = 'web',
):
    lock = TaskLockManager.force_release(task_id=task_id)
    if not lock:
        raise HTTPException(status_code=404, detail="Lock not found")
    message = f"Lock on '{task_id}' released" if lock else f"Lock on '{task_id}' not released"

    mesg = FlashMessage.add(request=request, message=message)

    if method == "web":
        return redirect_to_previous(request)
    else:
        return JSONResponse(content=mesg.to_dict())
