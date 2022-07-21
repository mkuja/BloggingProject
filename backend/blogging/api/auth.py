from flask.views import MethodView
from flask_smorest import Blueprint
from blogging.marshalling.schemas import Auth

from ..auxialiry.auth import login, logout, refresh

blp = Blueprint("Auth", "auth", url_prefix="/api/v1/auth", description="Operations on users")


@blp.route("/login")
class Login(MethodView):
    """User authentication."""

    @blp.arguments(Auth)
    @blp.response(200, Auth)
    def post(self, data):
        """Login.

        Login user with username and password."""
        if tokens := login(**data):
            return tokens, 200
        return {"message": "Invalid username or password."}, 401


@blp.route("/refresh")
class Refresh(MethodView):
    """Token refreshing."""

    @blp.response(200, Auth)
    @blp.response(401)
    def get(self):
        """Refresh token.

        Create a new token with refresh token. This new token can be used to
        access non-critical endpoints. For critical endpoints the user must
        have logged in recently with their credentials."""
        result = refresh()
        return result, 200 if "token" in result else 401


@blp.route("/logout")
class Logout(MethodView):
    """User token invalidation"""

    @blp.response(200)
    def get(self):
        """Logout user and invalidate all user tokens prior to this point in time.

        A JWT is required."""
        logout()
        return {"message": "Logged out on all devices."}


