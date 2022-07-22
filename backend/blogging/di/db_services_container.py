from os import getenv

import toml
from dependency_injector import containers, providers

from blogging.di.session_service import SessionService


class DBServicesContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    session_service = providers.Singleton(
        SessionService,
        connection_string=getenv("BLOG_DB_CONNECTION_STRING")
    )

db_services_container = DBServicesContainer()
db_services_container.wire(
    modules=["app", "blogging.auxialiry.auth"],
    packages=["blogging.auxialiry"]
)
db_services_container.config.from_dict(toml.load("settings.toml"))  # TODO: Remove this when settings are in DB.


