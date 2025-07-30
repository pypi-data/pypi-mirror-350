from typing import Annotated, Any

from fastpluggy.core.tools.inspect_tools import InjectDependency
from fastpluggy.fastpluggy import FastPluggy
from fastpluggy.core.menu.schema import MenuItem
from fastpluggy.core.module_base import FastPluggyBaseModule
from .config import AuthUserConfig
from .routers import router


class AuthUserPlugin(FastPluggyBaseModule):
    module_name :str= "auth_user"
    module_version :str= "0.0.1"
    module_settings :Any= AuthUserConfig

    module_mount_url :str= ""

    module_menu_name :str= "User Auth"
    module_menu_icon:str = "fa fa-user"
    module_menu_type :str= "no"

    module_router: Any = router  # Optional if you don’t use `.routes()`

    def on_load_complete(self, fast_pluggy: Annotated["FastPluggy", InjectDependency]) -> None:
        # todo: maybe use annotation
        fast_pluggy.menu_manager.add_menu_item(
            menu_type='user',
            item=MenuItem(url='/profile/', label="Profile", icon="fa-solid fa-user")
        )
        fast_pluggy.menu_manager.add_menu_item(
            menu_type='user',
            item=MenuItem(url='/logout', label="Logout", icon="fa-solid fa-sign-out-alt")
        )

    # Optional: routes() if you want to control it separately from module_router
    def routes(self):
        return [self.module_router]
