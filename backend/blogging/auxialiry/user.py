from functools import wraps
from typing import Dict, Union, Callable, Tuple

from dependency_injector.wiring import Provide
from flask_jwt_extended import get_jwt_identity
from passlib.hash import bcrypt
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from blogging.di.db_services_container import DBServicesContainer
from blogging.di.session_service import SessionService
from ..marshalling.schemas import UserSchema
from blogging.database.models import User


def create_user(name, username, email, password,
                session_service: SessionService = Provide[DBServicesContainer.session_service]):
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


def is_author(email: str, ssession: SessionService = Provide[DBServicesContainer.session_service]):
    """Check if email given has authority."""

    with ssession.session as session:
        stmt = (select(User)
                .where(User.email == email))
        user = session.scalar(stmt)
        return user.is_author


def jwt_identity_and_user_id_match(user_id,
                                   ssession: SessionService = Provide[DBServicesContainer.session_service]
                                   ) -> bool:
    with ssession.session as session:
        stmt = (select(User)
                .where(User.id == user_id))
        user: User = session.scalar(stmt)
        if user:
            return user.email == get_jwt_identity()
        return False


def author_required(route: Callable, ssession: SessionService = Provide[DBServicesContainer.session_service]):
    """This is the authorization decorator that checks whether client is an author."""

    @wraps(route)
    def inner(*args, ssession=ssession, **kwargs):
        identity = get_jwt_identity()
        stmt = (select(User)
                .where(User.email == identity))
        with ssession.session as session:
            user = session.scalar(stmt)
            if user.is_author:
                return route(*args, **kwargs)
            return {"message": "User needs author permissions to do this."}, 401

    return inner


def get_user_by_email(email: str,
                      sservice: SessionService = Provide[DBServicesContainer.session_service]
                      ) -> Union[Dict, None]:
    """Get user by email address."""

    stmt = (select(User)
            .where(User.email == email))
    with sservice.session as session:
        user = session.scalar(stmt)
        if user:
            return UserSchema().dump(user, many=False)
        return


def delete_user_by_id(id, sservice: SessionService = Provide[DBServicesContainer.session_service]
                      ) -> None:
    stmt = (delete(User)
            .where(User.id == id))
    with sservice.session as session:
        session.execute(stmt)
        session.commit()


def patch_user_by_id(new_data: Dict, id: int,
                     sservice: SessionService = Provide[DBServicesContainer.session_service]
                     ) -> Tuple[Dict[str, str], int]:
    stmt = (select(User)
            .where(User.id == id))
    with sservice.session as session:
        user = session.scalar(stmt)
        if user.email != get_jwt_identity():
            return {"message": "Unauthorized"}, 401
        for key, val in new_data.items():
            if key == "password":
                user.password_hash = bcrypt.hash(new_data["password"])
            if hasattr(user, key):
                setattr(user, key, val)
        session.add(user)
        session.commit()
        return UserSchema().dump(user)

