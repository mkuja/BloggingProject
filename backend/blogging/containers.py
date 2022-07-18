from os import getenv

import toml
from dependency_injector import containers, providers
from . import services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app"
        ],
        packages=[
            "blogging.api"
        ]
    )

    db_engine_service = providers.Factory(
        services.DatabaseEngineService,
        connection_string=getenv("BLOG_CONNECTION_STRING")
    )

    app_service = providers.Singleton(
        services.AppService,
        name="Blog"
    )


container = Container()
container.config.from_dict(toml.load("../settings.toml"))


