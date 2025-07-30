import contextlib
from typing import Optional

from elasticsearch import Elasticsearch

from elasticsearch_tools.connection.base.abc_session_manager import BaseSessionManager


class ElasticSessionManager(BaseSessionManager):
    def __init__(self) -> None:
        self._sessionmaker = None

    def init(self, url: str, login: Optional[str] = None, password: Optional[str] = None, **kwargs):
        """
        Init sessionmaker of elasticsearch database
        Args:
            url: elasticsearch host
            login: elasticsearch login if exists
            password: elasticsearch password if exists
        """
        print(f"Initial in {url}")
        self._sessionmaker = self._elastic_sessionmaker(url, login, password, **kwargs)

    @staticmethod
    def _elastic_sessionmaker(url: str, login: Optional[str] = None, password: Optional[str] = None, **kwargs):
        """
        Init elasticsearch session
        Args:
            url: elasticsearch host
            login: elasticsearch login if exists
            password: elasticsearch password if exists
        Returns:
            elasticsearch sessionmaker(function)
        """

        def get_client():
            print(f"Connecting elasticsearch in {url}")
            elasticsearch_kwargs = {"hosts": url}
            if login and password:
                elasticsearch_kwargs["http_auth"] = (login, password)

            if url.startswith("https://"):
                elasticsearch_kwargs["verify_certs"] = False

            client: Elasticsearch = Elasticsearch(**kwargs, **elasticsearch_kwargs)

            return client

        return get_client

    def close(self) -> None:
        """
        Delete sessionmaker of elasticsearch database
        Returns:
            None
        """
        self._sessionmaker = None

    def session(self) -> Elasticsearch:
        """
        Get session of elasticsearch database
        Returns:
            yield session of elasticsearch database
        """
        if self._sessionmaker is None:
            raise IOError("DatabaseSessionManager is not initialized")
        return self._sessionmaker()

    @contextlib.asynccontextmanager
    async def asession(self) -> Elasticsearch:
        """
        Get session of elasticsearch database
        Returns:
            yield session of elasticsearch database
        """
        if self._sessionmaker is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._sessionmaker() as session:
            yield session


elastic_db_manager = ElasticSessionManager()
