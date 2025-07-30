from sqlalchemy import Column, String, Boolean, TIMESTAMP, JSON
from starlette.authentication import BaseUser

from fastpluggy.core.database import Base


class FastPluggyBaseUser(Base, BaseUser):
    __tablename__ = "users"

    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return self._repr(id=self.id, username=self.username)

    @property
    def display_name(self) -> str:
        return self.username




class Session(Base):
    __tablename__ = 'sessions'

    sess_id = Column(String(255), primary_key=True, nullable=False)
    sess_data = Column(JSON, nullable=False)
    sess_lifetime = Column(TIMESTAMP(), nullable=False)
    sess_time = Column(TIMESTAMP(), nullable=False)
