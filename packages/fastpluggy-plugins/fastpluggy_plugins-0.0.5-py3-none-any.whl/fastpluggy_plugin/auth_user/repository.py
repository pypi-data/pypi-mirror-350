from loguru import logger

from .config import AuthUserConfig
from .auth.basic_auth import BasicAuthManager
from .models import FastPluggyBaseUser, Session
from datetime import datetime, timedelta
from sqlalchemy.orm import Session as DBSession  # alias to avoid conflict with our Session model


def initialize_admin_user(db):
    """
    Create a default admin user if no users exist in the database.
    """
    with db as session:
        user_count = session.query(FastPluggyBaseUser).count()
        if user_count == 0:
            settings_auth = AuthUserConfig()
            hashed_password = BasicAuthManager.hash_password(settings_auth.default_admin_password)

            admin_user =  FastPluggyBaseUser(
                username=settings_auth.default_admin_username,
                hashed_password=hashed_password,
                is_admin=True,
            )

            session.add(admin_user)
            session.commit()
            logger.info("Default admin user created with username 'admin' and password 'admin'.")




def create_or_update_session(db: DBSession, sess_id: str, sess_data: dict, lifetime_seconds: int):
    """
    Create or update a session record in the sessions table.

    Args:
        db (DBSession): The SQLAlchemy database session.
        sess_id (str): The unique session identifier.
        sess_data (dict): The session data to be stored (will be saved as JSON).
        lifetime_seconds (int): The lifetime of the session in seconds.

    Returns:
        The session record (instance of Session) that was created or updated.
    """
    now = datetime.utcnow()
    expiry_time = now + timedelta(seconds=lifetime_seconds)

    # Query for an existing session with the same ID.
    session_record = db.query(Session).filter(Session.sess_id == sess_id).first()

    if session_record:
        # Update the existing session.
        session_record.sess_data = sess_data
        session_record.sess_lifetime = expiry_time
        session_record.sess_time = now
    else:
        # Create a new session record.
        session_record = Session(
            sess_id=sess_id,
            sess_data=sess_data,
            sess_lifetime=expiry_time,
            sess_time=now
        )
        db.add(session_record)

    db.commit()
    return session_record
