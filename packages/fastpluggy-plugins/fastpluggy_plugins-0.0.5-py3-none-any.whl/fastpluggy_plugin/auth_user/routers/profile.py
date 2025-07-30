from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from fastpluggy.core.auth import require_authentication
from fastpluggy.core.dependency import get_templates

profile_router = APIRouter(prefix="/profile", tags=["profile"])



@profile_router.get("/", response_class=HTMLResponse)
async def profile(request: Request, templates=Depends(get_templates), user=Depends(require_authentication)):
    """
    Renders the user profile page.
    The `user` is provided by the authentication dependency.
    """
    return templates.TemplateResponse("auth_user/profile.html.j2", {"request": request, "user": user})
