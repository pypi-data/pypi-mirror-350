# plugin.py

from typing import Annotated, Any

from fastapi.routing import APIRoute
from fastpluggy.core.module_base import FastPluggyBaseModule
from fastpluggy.core.tools.inspect_tools import InjectDependency
from fastpluggy.fastpluggy import FastPluggy

from .config import CrudConfig
from .crud_admin_registry import CrudAdminRegistry

def get_crud_router():
    from .router import crud_router
    return crud_router

class CrudToolsModule(FastPluggyBaseModule):
    module_name : str= "crud_tools"
    module_menu_name: str = "CRUD"
    module_menu_type: str = "admin"
    module_version :str = "0.1.3"

    module_settings : Any = CrudConfig
    module_router :Any = get_crud_router

    extra_js_files :list= ['/app_static/crud_tools/js/dynamic-select.js']

    def after_setup_templates(self, fast_pluggy: Annotated[FastPluggy, InjectDependency]) -> None:
        # Register template helper
        from .template_tools import url_for_crud
        fast_pluggy.templates.env.globals["url_for_crud"] = url_for_crud

    def on_load_complete(self, fast_pluggy: Annotated[FastPluggy, InjectDependency]) -> None:

        # Extract all APIRoute paths tagged with "crud_tools"
        crud_routes = [
            route for route in fast_pluggy.app.routes
            if isinstance(route, APIRoute) and route.tags and "crud_tools" in route.tags and "front_action" in route.tags
        ]
        crud_routes_map = {route.name: route.path for route in crud_routes}
        FastPluggy.register_global('crud_routes', crud_routes_map)

        # Register the CRUD admin registry
        admin_registry = CrudAdminRegistry()
        FastPluggy.register_global("crud_admin_registry", admin_registry)
