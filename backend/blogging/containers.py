from os import getenv

import toml
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide
from . import services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()


    db_engine_service = providers.Factory(
        services.DatabaseEngineService,
        connection_string=getenv("BLOG_CONNECTION_STRING")
    )


container = Container()
container.config.from_dict(toml.load("../settings.toml"))

