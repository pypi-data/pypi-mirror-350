from functools import lru_cache
from typing import Optional

from elasticsearch import Elasticsearch

from .sync_session_manager import elastic_db_manager


@lru_cache(typed=True, maxsize=None)
async def get_elastic_client_generator() -> Elasticsearch:
    """
    Generator may be used in fastapi Depends, and inited in lifespan
    """
    async with elastic_db_manager.session() as session:
        return session


@lru_cache(typed=True, maxsize=None)
def get_elastic_client(url: str, login: Optional[str] = None, password: Optional[str] = None, **kwargs) -> Elasticsearch:
    """
    For sync class initializing
    Args:
        url: elasticsearch url, for example https://elastic-example:9200
        login: login is optional for auth
        password: login is optional for auth
        **kwargs: official kwargs from elasticsearch library exclude hosts

    Returns:

    """
    elastic_db_manager.init(url, login, password, **kwargs)
    return elastic_db_manager.session()