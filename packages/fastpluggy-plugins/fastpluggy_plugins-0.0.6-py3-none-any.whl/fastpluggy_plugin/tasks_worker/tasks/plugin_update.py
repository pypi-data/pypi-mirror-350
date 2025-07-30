from typing import Annotated

from fastpluggy.core.plugin.installer import PluginInstaller

from fastpluggy.core.routers.actions.modules import update_plugin_from_git
from fastpluggy.core.tools.inspect_tools import InjectDependency, call_with_injection
from fastpluggy.fastpluggy import FastPluggy
from loguru import logger

from ..config import TasksRunnerSettings
from ..task_registry import task_registry

@task_registry.register(name="check_for_plugin_updates", allow_concurrent=False)
def check_for_plugin_updates(
        fast_pluggy: Annotated[FastPluggy, InjectDependency]
):
    logger.info("Checking if update available for plugins!")
    installer = PluginInstaller(plugin_manager=fast_pluggy.get_manager())
    updates = installer.check_all_plugin_updates()
    ws_manager = None

    if updates:
        for update in updates:
            logger.info(f"Update available for plugin {update['plugin']} !")

            settings = TasksRunnerSettings()
            if settings.auto_update_plugins:
                logger.info(f"Updating plugin {update['plugin']} !")
                call_with_injection(
                    func=update_plugin_from_git,
                    context_dict={
                        FastPluggy: fast_pluggy,
                    },
                    user_kwargs={
                        'module_name': update['plugin'],
                     #   'type_module': 'plugin'
                    }
                )
                #if ws_manager:
                #    from websocket_tool.schema import WebSocketMessagePayload
                #    ws_manager.sync_broadcast(
                #        message=WebSocketMessagePayload(message=f"Plugin {update['name']} updated!", level="success")
                #    )

            else:
                pass
                #if ws_manager:
                #    from websocket_tool.schema import WebSocketMessagePayload
                #    ws_manager.sync_broadcast(
                #        message=WebSocketMessagePayload(message=f"Update available for plugin {update['name']} !")
                #    )


    else:
        logger.info("No update available for plugins!")
    return updates
