import logging
import os
from typing import Optional

from fastapi import APIRouter, Request
from fastapi import Body, Query
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse

from fastpluggy.core.flash import FlashMessage
from fastpluggy.core.tools.fastapi import redirect_to_previous
from fastpluggy.fastpluggy import FastPluggy
from ..schema.ws_message import WebSocketMessage

ws_router = APIRouter(
    prefix="/ws",
    tags=["websocket"]
)


@ws_router.websocket("/{client_id}")
@ws_router.websocket("")  # fallback if no client_id
async def websocket_endpoint(websocket: WebSocket, client_id: Optional[str] = None):
    manager = FastPluggy.get_global("ws_manager")
    if manager is not None:
        await manager.connect(websocket, client_id)

        try:
            while True:
                data = await websocket.receive_text()
                await manager.send_to_client(
                    WebSocketMessage(content=f"You wrote: {data}"),
                    client_id=client_id
                )
        except WebSocketDisconnect:
            manager.disconnect(client_id if client_id else websocket)


@ws_router.post("/send-message")
async def send_message(
    request: Request,
    payload: WebSocketMessage = Body(...),
        method: str = 'web',
):
    manager = FastPluggy.get_global("ws_manager")

    if not manager.active_connections and not manager.unnamed_connections:
        FlashMessage.add(request=request, message="No active WebSocket connections", category='error')
    else:
        await manager.broadcast(payload)
        FlashMessage.add(request=request, message="Message broadcasted to all connected WebSocket clients", category="success")

    if method == "web":
        return redirect_to_previous(request)
    else:
        return JSONResponse(content=payload.to_json())

# @ws_router.get("/get_sw_version.js")
# async def get_sw_version(module_manager=Depends(get_module_manager)):
#     from websocket_tool import WebSocketToolPlugin
#     module = WebSocketToolPlugin
#     module_version =module.module_version
#     js = f'''
#     window.SW_VERSION = "{module_version}";
#     window.SW_READY = Promise.resolve(window.SW_VERSION);
#     '''
#     return Response(content=js, media_type="application/javascript")

@ws_router.get("/service-worker.js")
async def service_worker(v: str = Query(None)):
    logging.info(f"service worker {v} requested")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = f"{base_dir}/../static/js/service-worker.js"
    response = FileResponse(file_path)
    response.headers["Service-Worker-Allowed"] = "/"
    return response