# core/auth/session_auth.py

from fastapi import Request, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from fastpluggy.core.auth.auth_interface import AuthInterface
from fastpluggy.core.database import get_db
from ..models import FastPluggyBaseUser


class SessionAuthManager(AuthInterface):
    login_redirect : bool = True
    login_url : str = "/login"
    logout_url : str = "/logout"

    async def on_authenticate_error(self, request: Request):
        if self.login_redirect:
            raise HTTPException(
                status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                detail="Not authenticated",
                headers={"Location": self.login_url}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

    # async def authenticate(self, request: Request) -> FastPluggyBaseUser:
    #     user_id = request.session.get("user_id")
    #     if not user_id:
    #         return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    #     db: Session = next(get_db())
    #     user = db.query(FastPluggyBaseUser).get(user_id)
    #     if not user:
    #         return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    #     return user
    # async def authenticate(self, request: Request) -> Optional[Tuple[BaseUser, AuthCredentials]]:
    #     # Retrieve user ID from the session.
    #     user_id = request.session.get("user_id")
    #     if not user_id:
    #         # No user id found; authentication not provided.
    #         return None
    #
    #     # Retrieve the database session.
    #     # Adjust this according to how your application attaches a DB session.
    #     db: Session = next(get_db())
    #     user = db.query(User).get(user_id)
    #     if not user:
    #         # User not found; authentication fails.
    #         return None
    #
    #     # If a user is found, return a tuple of ( credentials, user )
    #     return AuthCredentials(["authenticated"]), user
