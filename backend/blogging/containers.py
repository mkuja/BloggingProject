from os import getenv

import toml
from dependency_injector import containers, providers

from . import services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app",
            "blogging.database.models"
        ],
        packages=[
            "blogging.auxialiry",
        #    "blogging.database.alembic"
        ]
    )

    session_service = providers.Singleton(
        services.SessionService,
        connection_string=getenv("BLOG_DB_CONNECTION_STRING")
    )

    app_settings = providers.Singleton(
        services.AppSettingsService
    )

container = Container()
container.config.from_dict(toml.load("settings.toml"))  # TODO: Remove this when settings are in DB.


