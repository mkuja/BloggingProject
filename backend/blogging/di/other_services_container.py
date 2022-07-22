from dependency_injector import providers, containers

from blogging.di.settings_service import AppSettingsService


class DBServicesContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        modules=[
            #"app",
            #"blogging.database.models"
        ],
        packages=[
            #"blogging.auxialiry",
        #    "blogging.database.alembic"
        ]
    )

    app_settings = providers.Singleton(
        AppSettingsService
    )


other_services_container = DBServicesContainer()

