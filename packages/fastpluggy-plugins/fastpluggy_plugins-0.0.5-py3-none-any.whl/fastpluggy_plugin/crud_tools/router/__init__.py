from fastapi import APIRouter, Depends

from fastpluggy.core.auth import require_authentication
from .api import crud_api_router
from .crud import crud_view_router
from .crud_admin import crud_admin_view_router
from ..config import CrudConfig

auth_dependencies = []
settings = CrudConfig()
if settings.require_authentication:
    auth_dependencies.append(Depends(require_authentication))

crud_router = APIRouter(dependencies=auth_dependencies)
crud_router.include_router(crud_view_router)
crud_router.include_router(crud_api_router)
crud_router.include_router(crud_admin_view_router)