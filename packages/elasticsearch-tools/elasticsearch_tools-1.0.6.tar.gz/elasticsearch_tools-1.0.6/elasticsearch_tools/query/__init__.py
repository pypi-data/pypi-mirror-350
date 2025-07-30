from typing import Optional

from .base import ElasticBaseQuery
from .bool import ElasticBoolMust, ElasticBoolMustNot, ElasticBoolQuery, ElasticBoolShould
from .search import (
    ElasticExistsQuery,
    ElasticFullMatchQuery,
    ElasticFuzzyQuery,
    ElasticGeoPointQuery,
    ElasticGeoPointRangeQuery,
    ElasticMatchQuery,
    ElasticNestedQuery,
    ElasticQueryString,
    ElasticRangeQuery,
    ElasticSearchQuery,
    ElasticTermQuery,
)

queries = dict()

for bool_query in ElasticBoolQuery.__subclasses__():
    queries[bool_query.query_type] = bool_query

for search_query in ElasticSearchQuery.__subclasses__():
    queries[search_query.query_type] = search_query


def generate_query(_type: Optional[str], *args, **kwargs):
    if _type:
        query_class = queries.get(_type)
        return query_class(*args, **kwargs)
    return dict(**kwargs)
