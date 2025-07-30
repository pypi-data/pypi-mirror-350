from fastapi import APIRouter, Depends

from ..routers.login import login_router
from ..routers.profile import profile_router
from fastpluggy.core.auth import require_authentication

router =  APIRouter(
    tags=["auth_user"],
)

router.include_router(login_router)
router.include_router(profile_router,dependencies=[Depends(require_authentication)],)