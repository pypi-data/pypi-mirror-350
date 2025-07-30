import logging
import os

from fastapi import APIRouter, Query, Depends
from fastapi.responses import FileResponse

from fastpluggy.core.dependency import get_module_manager
from .admin import ws_admin_router
from .ws import ws_router

ws_tool_router = APIRouter(
    tags=["websocket"]
)

ws_tool_router.include_router(ws_router)
ws_tool_router.include_router(ws_admin_router)


@ws_tool_router.get("/sw_info.json")
async def get_sw_info(module_manager=Depends(get_module_manager)):
    from ..plugin import WebSocketToolPlugin
    module = WebSocketToolPlugin()
    module_version =module.module_version
    return {"version": module_version}


@ws_tool_router.get("/service-worker.js")
async def service_worker(v: str = Query(None)):
    logging.info(f"service worker {v} requested")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "../static/service-worker.js")
    response = FileResponse(file_path)
    response.headers["Service-Worker-Allowed"] = "/"
    return response

