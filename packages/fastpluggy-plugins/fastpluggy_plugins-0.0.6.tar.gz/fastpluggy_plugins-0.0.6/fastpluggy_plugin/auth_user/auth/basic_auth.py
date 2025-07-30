from typing import Type

import bcrypt
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from ..models import FastPluggyBaseUser
from fastpluggy.core.auth.auth_interface import AuthInterface
from fastpluggy.core.database import get_db

security = HTTPBasic()

class BasicAuthManager(AuthInterface):

    @property
    def user_model(self) -> Type[FastPluggyBaseUser]:
        return FastPluggyBaseUser

    @staticmethod
    def verify_password( plain_password: str, hashed_password: str):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def hash_password(password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    async def on_authenticate_error(self, request: Request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    async def authenticate(self, request: Request) -> FastPluggyBaseUser:
        try:
            # Retrieve credentials from the request
            credentials: HTTPBasicCredentials = await security(request)
        except Exception:
            return None
        db: Session = next(get_db())
        user = db.query(FastPluggyBaseUser).filter(FastPluggyBaseUser.username == credentials.username).first()
        auth_ok = not user or not BasicAuthManager.verify_password(credentials.password, user.hashed_password)
        db.close()
        if auth_ok:
            return None
        role = "admin" if user.is_admin else "user"
        return [role], user
