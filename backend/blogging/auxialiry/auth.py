import datetime
import time
from datetime import timedelta
from typing import Union, Dict, Tuple

from dependency_injector.wiring import Provide
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    create_refresh_token, get_jwt_header
)
from passlib.hash import bcrypt

from app import jwt
from blogging.auxialiry.user import get_user_by_email
from blogging.containers import Container
from blogging.database.models import User

from sqlalchemy import select

from blogging.marshalling.schemas import UserSchema
from blogging.services import SessionService


def login(username,
          password,
          session_service=Provide[Container.session_service]
          ) -> Union[Dict[str, str] | bool]:
    """Return a fresh JWT on successful login, False otherwise."""

    stmt = (select(User)
            .where(User.username == username))
    with session_service.session as session:
        user_from_db: User = session.scalar(stmt)
        if not user_from_db:
            return False
        if bcrypt.verify(password, user_from_db.password_hash):
            claims = {"is_author": user_from_db.is_author}
            return {"token": create_access_token(identity=user_from_db.email,
                                                 fresh=True,
                                                 expires_delta=timedelta(minutes=15),
                                                 additional_claims=claims),
                    "refresh_token": create_refresh_token(identity=user_from_db.email,
                                                          additional_claims=claims)}
        return False


def refresh(ssession: SessionService = Provide[Container.session_service]
            ) -> Tuple[Dict[str, str], int]:
    identity = get_jwt_identity()
    stmt = (select(User)
            .where(User.email == identity))
    with ssession.session as session:
        user = session.scalar(stmt)
        if not user:
            return {"message": "Error: No such user."}, 404
        claims = {"is_author": user.is_author}
        token = create_access_token(fresh=False,
                                    expires_delta=timedelta(minutes=20),
                                    additional_claims=claims)
        return {"token": token}, 200


@jwt_required()
def logout(sservice: SessionService = Provide[Container.session_service]) -> bool:
    """Invalidate all user tokens prior to this point in time.

    A JWT is required for this.
    """

    identity = get_jwt_identity()
    stmt = (select(User)
            .where(User.email == identity))
    with sservice.session as session:
        user_from_db: User = session.scalar(stmt)
        if not user_from_db:
            return False
        user_from_db.last_logged_out = time.time()
        session.add(user_from_db)
        session.commit()
        return True


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    iat = jwt_payload["iat"]
    sub = jwt_payload["sub"]
    user = get_user_by_email(sub)
    if not user:
        return False
    return iat < user["last_logged_out"]
