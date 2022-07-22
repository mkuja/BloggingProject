from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class SessionService:

    def __init__(self, connection_string, *args, **kwargs):
        """
        :param connection_string: ex. "postgresql+asyncpg://scott:tiger@localhost/test"
        :param args:
        :param kwargs: ex. echo=True
        """
        self._engine = create_engine(connection_string, *args, **kwargs)
        self._session = Session(self._engine)

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._session


