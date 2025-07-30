import inspect
from typing import List, Dict

from fastapi import APIRouter, Request, Depends
from loguru import logger

from fastpluggy.core.database import Base
from fastpluggy.core.dependency import get_view_builder, get_fastpluggy
from fastpluggy.core.menu.decorator import menu_entry
from fastpluggy.core.models_tools.sqlalchemy import ModelToolsSQLAlchemy
from fastpluggy.core.tools.inspect_tools import get_module
from fastpluggy.core.view_builer.components.table import TableView

crud_admin_view_router = APIRouter(prefix='/models', tags=["front_action"])


def get_sqlalchemy_models(module_name: str) -> list[type]:
    module = get_module(f"{module_name}.models", reload=False)
    return [
        obj for name, obj in inspect.getmembers(module)
        if inspect.isclass(obj) and ModelToolsSQLAlchemy.is_sqlalchemy(obj) and obj is not Base
    ]


def get_admin_model_status(module_name: str) -> List[Dict[str, str]]:
    result = []
    models = get_sqlalchemy_models(module_name)
    for model in models:
        from ..router.crud import get_admin_instance
        admin = get_admin_instance(model.__name__, default_crud_class=False)
        result.append({
            "module_name": module_name,
            "model_name": model.__name__,
            "registered": admin is not None,
            "admin_class": admin.__class__.__name__ if admin else None
        })
    return result


@menu_entry(label="Models", type='admin')
@crud_admin_view_router.api_route("", methods=["GET", "POST"], name="list_models")
async def list_models(request: Request, view_builder=Depends(get_view_builder),
                      fast_pluggy=Depends(get_fastpluggy)):
    items_admin = []
    for module_name in fast_pluggy.module_manager.modules.values():
        try:
            admin = get_admin_model_status(module_name.package_name)
            items_admin.extend(admin)
        except Exception as e:
            logger.exception(e)

    from ..crud_link_helper import CrudLinkHelper
    from ..schema import CrudAction
    items = [
        TableView(
            data=items_admin,
            title="Crud Models",
            links=[
                CrudLinkHelper.get_crud_link(model='<model_name>', action=CrudAction.LIST),
            ]
        )
    ]

    return view_builder.generate(
        request,
        title="List of models",
        items=items,
    )
