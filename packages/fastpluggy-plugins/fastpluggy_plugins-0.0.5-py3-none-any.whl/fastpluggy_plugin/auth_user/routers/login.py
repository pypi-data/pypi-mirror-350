from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

login_router = APIRouter()



@login_router.get("/logout", name="logout")
async def logout(request: Request):
    request.session.clear()  # Clears session data
    return RedirectResponse(url="/login", status_code=303)  # Redirect to login page
