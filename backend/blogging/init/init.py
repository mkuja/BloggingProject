from dependency_injector.wiring import inject, Provide
from flask import Flask

from blogging.auxialiry.misc import set_app_settings, get_app_settings
import blogging.api.auth as auth_api
import blogging.api.blog_post as blog_post_api
import blogging.api.comment as comment_api
import blogging.api.user as user_api
import blogging.api.settings as settings_api
from blogging.converters import DateConverter
from blogging.di.api_service import ApiService
from blogging.di.other_services_container import AppServicesContainer


@inject
def init(service: ApiService = Provide[AppServicesContainer.api_service]) -> Flask:

    # Register custom date converter
    service.app.url_map.converters['date'] = DateConverter

    # Define custom converter to schema function
    def date_to_params_schema(converter):
        return {'type': 'string', 'format': 'dd-mm-yyyy'}

    # Register DateConverter path converter in Api
    service.api.register_converter(
        DateConverter,
        date_to_params_schema
    )

    # Make default settings if necessary
    if not (settings := get_app_settings()):
        set_app_settings()

    service.api.register_blueprint(user_api.blp)
    service.api.register_blueprint(auth_api.blp)
    service.api.register_blueprint(blog_post_api.blp)
    service.api.register_blueprint(comment_api.blp)
    service.api.register_blueprint(settings_api.blp)

    return service.app
