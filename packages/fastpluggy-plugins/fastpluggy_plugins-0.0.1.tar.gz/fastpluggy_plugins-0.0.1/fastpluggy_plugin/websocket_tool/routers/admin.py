from fastapi import Request, Depends, APIRouter

from fastpluggy.core.dependency import get_view_builder
from fastpluggy.core.menu.decorator import menu_entry
from fastpluggy.core.view_builer.components.debug import DebugView
from fastpluggy.core.view_builer.components.table import TableView
from fastpluggy.fastpluggy import FastPluggy

ws_admin_router = APIRouter()

@menu_entry(label="WS Clients", type='admin', icon="fa-solid fa-network-wired")
@ws_admin_router.get("/clients", name="websocket_clients_dashboard")
async def websocket_clients_dashboard(request: Request, view_builder=Depends(get_view_builder)):
    manager = FastPluggy.get_global("ws_manager")
    clients = manager.list_clients()

    return view_builder.generate(
        request,
        title="WebSocket Clients",
        items=[
            TableView(
                title="Connected Clients",
                data=clients,
                field_callbacks={
                    "client_id": lambda val: f"<code>{val}</code>",
                    "type": lambda val: f"<span class='badge bg-info'>{val}</span>",
                },
            ),
            DebugView(data=clients, collapsed=True),
            #ListButtonView(buttons=[
            #    AutoLinkView(label="Back to Dashboard", route_name="dashboard_tasks_worker")
            #])
        ]
    )
