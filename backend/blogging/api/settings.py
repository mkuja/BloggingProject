from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from blogging.auxialiry.misc import get_app_settings, set_app_settings
from blogging.auxialiry.user import author_required
from blogging.marshalling.schemas import SettingsSchema

blp = Blueprint("Settings", "settings", url_prefix="/api/v1/app_settings", description="Get and set settings.")


@blp.route("/")
class Settings(MethodView):

    @jwt_required(optional=True)
    @blp.response(200, SettingsSchema)
    def get(self):
        """Get application settings.

        Open for all clients."""
        return get_app_settings(), 200

    @jwt_required()
    @author_required
    @blp.response(201, SettingsSchema)
    @blp.arguments(SettingsSchema)
    def post(self, data):
        """Set application settings.

        Open only for the author."""
        set_app_settings(**data)
        return get_app_settings(), 201

