from flask.views import MethodView
from flask_smorest import Blueprint
from blogging.marshalling.schemas import Auth

from ..auxialiry.auth import login


blp = Blueprint("Auth", "auth", url_prefix="/api/v1/auth", description="Operations on users")


@blp.route("/")
class Auth(MethodView):
    """User authentication."""

    @blp.arguments(Auth)
    @blp.response(200, Auth)
    def post(self, data):
        """Login.

        Login user with username and password."""
        if token := login(**data):
            print(token)
            return {"token": token}, 200
        return {"message": "Invalid username or password."}, 401
