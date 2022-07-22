from typing import Dict, Any, Union

from dependency_injector.wiring import Provide
from sqlalchemy import select

from blogging.database.models import Settings
from blogging.di.db_services_container import DBServicesContainer
from blogging.di.session_service import SessionService
from blogging.marshalling.schemas import SettingsSchema


def set_app_settings(service: SessionService = Provide[DBServicesContainer.session_service],
                     **settings: Dict[str, Any]
                     ) -> None:
    """Set application settings.

    `set_settings` takes number of kwargs which are the app settings.

    :argument anonymous_can_comment: Boolean
    :argument users_can_register: Boolean
    :argument verify_email: Boolean
    :argument show_social_media_shares
    :argument use_comment_captcha_for_anonymous: Boolean
    :argument use_comment_captcha_for_registered: Boolean
    :argument date_and_time_format: Str, The format is described at:
    https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior"""

    # Try get latest settings from DB
    stmt = (select(Settings)
            .order_by(Settings.id)
            .limit(1))
    with service.session as session:
        latest_settings = session.scalar(stmt)
        if not latest_settings:
            new_settings = Settings(**settings)
        else:
            serialized: Dict = SettingsSchema().dump(latest_settings)
            serialized.update(settings)
            new_settings = Settings(**settings)
        session.add(new_settings)
        session.commit()


def get_app_settings(service: SessionService = Provide[DBServicesContainer.session_service]
                     ) -> Union[Dict[str, Any], None]:
    """Get application settings.

    :returns A dict with same keys as what is passed as keyword arguments for set_app_settings()."""

    stmt = (select(Settings)
            .order_by(Settings.id.desc())
            .limit(1))
    with service.session as session:
        settings = session.scalar(stmt)
        return SettingsSchema().dump(settings)
