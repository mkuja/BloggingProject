import os

from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_smorest import Api


def load_blog_dotenv(secrets_file: str):
    load_dotenv(secrets_file)


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

import blogging.containers as containers
import blogging.api.user as user_api
import blogging.api.auth as auth

api.register_blueprint(user_api.blp)
api.register_blueprint(auth.blp)

