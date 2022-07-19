from typing import Dict

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from blogging.auxialiry.user import create_user, get_user_by_email
from blogging.marshalling.schemas import UserSchema
import blogging.database.models as models


blp = Blueprint("UserSchema", "users", url_prefix="/api/v1/user", description="Operations on users")


@blp.route("/")
class User(MethodView):

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, data: Dict):
        """Add a new user.
        """
        user: Dict = create_user(**data)
        if "id" in user.keys():
            return user, 201
        else:
            return user, 200

    @jwt_required(optional=True)
    def get(self):
        """Get current user.
        
        JWT is optional. If no JWT is present in the request, it will give
        anonymous user.
        """
        identity = get_jwt_identity()
        if identity:
            return get_user_by_email(get_jwt_identity()), 200
        return {"username": "Anonymous", "name": "Anonymous"}, 200



@blp.route("/<id>")
class UserById(MethodView):

    @blp.response(204)
    def delete(self, id):
        """Delete user by id.

        A fresh JWT is required. The JWT has to be either author's or its owner's."""
        pass

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def patch(self, data, id):
        """Alter user by id.

        A fresh JWT is required."""
        print(data, id)  # TODO: Implement this.
