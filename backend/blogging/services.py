from random import choices
from string import ascii_letters, punctuation
from typing import Dict, Any

from dependency_injector.wiring import Provide, Container
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from blogging.database.models import Settings
from blogging.marshalling.schemas import Settings as SettingsSchema


class SessionService:

    def __init__(self, connection_string, *args, **kwargs):
        """
        :param connection_string: ex. "postgresql+asyncpg://scott:tiger@localhost/test"
        :param args:
        :param kwargs: ex. echo=True
        """
        self._engine = create_engine(connection_string, *args, **kwargs)
        self._session = Session(self._engine)

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._session


class SettingsTableIsEmpty(Exception):
    """Settings table is empty when it was not expected."""

    pass


class AppSettingsService:

    @staticmethod
    def get_current_settings(ssession: SessionService = Provide[Container.session_service]
                             ) -> Settings:
        stmt = (select(Settings)
                .order_by(Settings.id)
                .limit(1))
        with ssession.session as session:
            settings = session.execute(stmt)
            if not settings:
                raise SettingsTableIsEmpty("Settings is empty. Need settings to get them.")
            return SettingsSchema().dump(settings)

    @staticmethod
    def save_setting(settings: Dict[str, Any],
                     ssession: SessionService = Provide[Container.session_service]
                     ) -> Settings:
        """Save settings.

        :arg settings: Check the database model to see what this dict should contain."""

        with ssession.session as session:
            to_db = Settings(**settings)
            session.add(to_db)
            session.commit()
            return SettingsSchema().dump(to_db)

    @staticmethod
    def get_jwt_secret_key(generate=False, ssession: SessionService = Provide[Container.session_service]
                           ) -> str:
        if generate:
            return "".join(choices(ascii_letters + punctuation, k=80))

        with ssession.session as session:
            stmt = (select(Settings)
                    .order_by(Settings.id)
                    .limit(1))
            print(stmt)
            settings = session.scalar(stmt)
            if not settings:
                return "".join(choices(ascii_letters + punctuation, k=80))

            return settings.jwt_secret_key


