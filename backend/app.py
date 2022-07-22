import os

from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from blogging.converters import DateConverter


def load_blog_dotenv():
    load_dotenv(".env")


app = Flask(__name__)
app.config["API_TITLE"] = "Blogging backend"
app.config["API_VERSION"] = "1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/api/v1/"
app.config["OPENAPI_REDOC_PATH"] = "/redoc"
app.config["OPENAPI_REDOC_URL"] = "https://cdn.jsdelivr.net/npm/redoc@2.0.0-alpha.17/bundles/redoc.standalone.js"
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


jwt = JWTManager(app)
api = Api(app)


# Register custom date converter
app.url_map.converters['date'] = DateConverter


# Define custom converter to schema function
def date_to_params_schema(converter):
    return {'type': 'string', 'format': 'dd-mm-yyyy'}


# Register converter in Api
api.register_converter(
    DateConverter,
    date_to_params_schema
)


import blogging.api.user as user_api
import blogging.api.auth as auth_api
import blogging.api.blog_post as blog_post_api
import blogging.api.comment as comment_api

api.register_blueprint(user_api.blp)
api.register_blueprint(auth_api.blp)
api.register_blueprint(blog_post_api.blp)
api.register_blueprint(comment_api.blp)

