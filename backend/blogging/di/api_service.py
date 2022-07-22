import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api


class ApiService:

    def __init__(self):
        self._app = Flask("app")
        self._app.config["API_TITLE"] = "Blogging backend"
        self._app.config["API_VERSION"] = "1"
        self._app.config["OPENAPI_VERSION"] = "3.0.2"
        self._app.config["OPENAPI_URL_PREFIX"] = "/api/v1/"
        self._app.config["OPENAPI_REDOC_PATH"] = "/redoc"
        self._app.config[
            "OPENAPI_REDOC_URL"] = "https://cdn.jsdelivr.net/npm/redoc@2.0.0-alpha.17/bundles/redoc.standalone.js"
        self._app.config["JWT+-_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
        self._api = Api(self._app)

        self._jwt = JWTManager(self._app)

    @property
    def app(self):
        return self._app

    @property
    def api(self):
        return self._api

    @property
    def jwt(self):
        return self._jwt
