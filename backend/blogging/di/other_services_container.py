from dependency_injector import providers, containers

from blogging.di.api_service import ApiService
# from blogging.di.settings_service import AppSettingsService


class AppServicesContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app",
            "blogging.auxialiry.auth",
            #"blogging.database.models"
        ],
        packages=[
            #"blogging.auxialiry",
        #    "blogging.database.alembic"
        ]
    )

    # app_settings = providers.Singleton(
    #     AppSettingsService
    # )

    api_service = providers.Singleton(
        ApiService
    )


app_services_container = AppServicesContainer()
print("AUTO-WIRING AppServicesContainer:", app_services_container.is_auto_wiring_enabled())

