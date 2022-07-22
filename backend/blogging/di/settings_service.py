from random import choices
from string import ascii_letters, punctuation
from typing import Dict, Any

from dependency_injector.wiring import Provide
from sqlalchemy import select

from blogging.containers import Container
from blogging.database.models import Settings
from blogging.session_service import SessionService
from blogging.marshalling.schemas import Settings as SettingsSchema


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

