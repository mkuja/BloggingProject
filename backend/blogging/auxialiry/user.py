from typing import Dict

from dependency_injector.wiring import Provide
from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from blogging.containers import Container
from blogging.database.models import User
from blogging.services import SessionService
from ..marshalling.schemas import UserSchema


def create_user(name, username, email, password,
                session_service: SessionService = Provide[Container.session_service]):
    """Create user with username."""

    try:
        with session_service.session as session:
            hash_ = bcrypt.hash(password)
            user = User(name=name, username=username, email=email, password_hash=hash_)
            session.add(user)
            session.commit()
            return UserSchema().dump(user, many=False)
    except IntegrityError as e:
        return {"message": "Email is already registered."}


def get_user_by_email(email: str,
                      sservice: SessionService = Provide[Container.session_service]
                      ) -> Dict:
    """Get user by email address."""

    stmt = (select(User)
            .where(User.email == email))
    with sservice.session as session:
        user = session.scalar(stmt)
        if user:
            return UserSchema().dump(user, many=False)
        return
