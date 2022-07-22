from dependency_injector import providers, containers

from blogging import auxialiry
from blogging.di.api_service import ApiService
# from blogging.di.settings_service import AppSettingsService


class AppServicesContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    api_service = providers.Singleton(
        ApiService
    )


app_services_container = AppServicesContainer()
# print("AUTO-WIRING AppServicesContainer:", app_services_container.is_auto_wiring_enabled())

