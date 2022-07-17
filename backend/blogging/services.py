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
