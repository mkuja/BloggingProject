from typing import Dict

import flask
from asgiref.wsgi import WsgiToAsgi
from sqlalchemy.ext.asyncio import create_async_engine


class DatabaseEngineService:

    def __init__(self, connection_string, *args, **kwargs):
        """
        :param connection_string: ex. "postgresql+asyncpg://scott:tiger@localhost/test"
        :param args:
        :param kwargs: ex. echo=True
        """
        self._engine = create_async_engine(connection_string, *args, **kwargs)

    @property
    def engine(self):
        return self._engine


class AppService:

    def __init__(self, name, *args, asgi: bool = True, **kwargs):
        """
        :param name: Name for Flask()
        :param args: Other args for Flask()
        :param kwargs: Other kwargs for Flask()
        """
        if asgi:
            self._app = WsgiToAsgi(flask.Flask(name))
        else:
            self._app = flask.Flask(name)

    @property
    def app(self):
        return self._app

    def configure(self, config: Dict):
        self.app.config.update(config)
