import logging
from typing import Annotated, Any

from fastpluggy.core.tools.inspect_tools import InjectDependency
from fastpluggy.core.module_base import FastPluggyBaseModule
from fastpluggy.fastpluggy import FastPluggy

from .routers import ws_tool_router


class WebSocketToolPlugin(FastPluggyBaseModule):
    module_name :str= "websocket_tool"
    module_version :str= "0.0.2"

    module_menu_name :str= "WebsocketTool"
    module_menu_icon :str= "fa-solid fa-rss"
    module_menu_type :str= "no"
    module_mount_url:str = ""

    module_router:Any = ws_tool_router

    extra_js_files :list = [
      #  "/ws/get_sw_version.js",
        "/app_static/websocket_tool/scripts.js",
        "/app_static/websocket_tool/ws-registry.js"
    ]

    def on_load_complete(self, fast_pluggy: Annotated[FastPluggy, InjectDependency]) -> None:
        from .ws_manager import ConnectionManager
        ws_manager = ConnectionManager()
        FastPluggy.register_global("ws_manager", ws_manager)

        try:
            if fast_pluggy.module_manager.is_module_loaded("tasks_worker"):
                from fastpluggy_plugin.tasks_worker.notifiers.registry import register_notifier, register_global_notification_rules
                from fastpluggy_plugin.tasks_worker.schema.task_event import TaskEvent
                from .notifiers.websocket import WebSocketNotifier

                websocket = WebSocketNotifier(config={}, events=[TaskEvent.ALL])
                register_notifier(websocket)

                register_global_notification_rules([
                    {
                        "name": websocket.name,
                        "events": ["*"]
                    }
                ])
            else:
                logging.info("Module 'tasks_worker' not loaded, skipping notifier setup.")

        except Exception as e:
            logging.exception("Error initializing notifier for WebSocketTool")
