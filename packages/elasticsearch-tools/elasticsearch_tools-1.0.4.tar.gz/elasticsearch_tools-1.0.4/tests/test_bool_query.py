import pytest

from elasticsearch_tools.query import ElasticBoolMust, ElasticBoolMustNot, ElasticBoolShould, ElasticFuzzyQuery


@pytest.mark.parametrize(
    "query_class, negative_query_class",
    [
        (ElasticBoolMustNot, ElasticBoolMust),
        (ElasticBoolMust, ElasticBoolMustNot)
    ],
)
def test_denial(query_class, negative_query_class):
    query = query_class([])
    reversed_negative_query = ~negative_query_class([])
    assert query.get_query() == reversed_negative_query.get_query()


def test_denial_should():
    auto_should_not_query = ~ElasticBoolShould([])
    should_not_query = ElasticBoolMustNot([ElasticBoolShould([])])
    assert auto_should_not_query.get_query() == should_not_query.get_query()


@pytest.mark.parametrize(
    "query_class, query",
    [
        (ElasticBoolMustNot, {"bool": {"must_not": []}}),
        (ElasticBoolMust, {"bool": {"must": []}}),
        (ElasticBoolShould, {"bool": {"should": []}})
    ],
)
def test_query_writing(query_class, query):
    auto_query = query_class([])
    assert auto_query.get_query() == query


@pytest.mark.parametrize(
    "query_class, query",
    [
        (ElasticBoolMustNot, {'bool': {'should': [{'bool': {'must_not': []}}, {'bool': {'must_not': []}}]}}),
        (ElasticBoolMust, {"bool": {"should": [{"bool": {"must": []}}, {"bool": {"must": []}}]}}),
        (ElasticBoolShould, {"bool": {"should": []}})
    ],
)
def test_query_or(query_class, query):
    auto_query = query_class([])
    new_query = auto_query | auto_query
    assert new_query.get_query() == query

    new_query = query_class([])
    new_query |= auto_query
    assert new_query.get_query() == query


@pytest.mark.parametrize(
    "query_class, query",
    [
        (ElasticBoolMustNot, {'bool': {'must': [{'bool': {'must_not': []}}, {'bool': {'must_not': []}}]}}),
        (ElasticBoolMust, {"bool": {"must": []}}),
        (ElasticBoolShould, {"bool": {"must": [{"bool": {"should": []}}, {"bool": {"should": []}}]}})
    ],
)
def test_query_and(query_class, query):
    auto_query = query_class([])
    new_query = auto_query & auto_query
    assert new_query.get_query() == query

    new_query = query_class([])
    new_query &= auto_query
    assert new_query.get_query() == query


@pytest.mark.parametrize(
    "query_class, query",
    [
        (ElasticBoolMustNot, {"bool": {"must": []}}),
        (ElasticBoolMust, {"bool": {"must_not": []}}),
        (ElasticBoolShould, {"bool": {"must_not": [{"bool": {"should": []}}]}})
    ],
)
def test_query_not(query_class, query):
    auto_query = ~query_class([])
    assert auto_query.get_query() == query


@pytest.mark.parametrize(
    "query_class",
    [
        ElasticBoolMustNot,
        ElasticBoolMust,
        ElasticBoolShould
    ],
)
def test_query_getitem(query_class):
    query = query_class([ElasticFuzzyQuery(field="f", value="v")])
    first_query = query[0]
    assert isinstance(first_query, ElasticFuzzyQuery)
    assert first_query.get_query() == {"fuzzy": {"f": "v"}}