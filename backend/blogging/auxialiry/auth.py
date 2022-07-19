from datetime import timedelta
from typing import Union

from dependency_injector.wiring import Provide
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt

from blogging.containers import Container
from blogging.database.models import User

from sqlalchemy import select


def login(username,
          password,
          session_service = Provide[Container.session_service]) -> Union[str | bool]:
    """Return a fresh JWT on successful login, False otherwise."""

    stmt = (select(User)
            .where(User.username == username))
    with session_service.session as session:
        user_from_db: User = session.scalar(stmt)
        if not user_from_db:
            return False
        if bcrypt.verify(password, user_from_db.password_hash):
            claims = {"is_author": user_from_db.is_author}
            return create_access_token(identity=user_from_db.email,
                                       fresh=True,
                                       expires_delta=timedelta(minutes=15),
                                       additional_claims=claims)
        return False

