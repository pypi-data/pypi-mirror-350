import pytest

from elasticsearch_tools import query as q

@pytest.mark.parametrize(
    "auto_query, query",
    [
        (q.ElasticQueryString(field="f", value="v"), {"query_string": {"default_field": "f", "query": "v"}}),
        (q.ElasticQueryString(field="f"), {"query_string": {"default_field": "f", "query": "*"}}),
        (q.ElasticQueryString(value="v"), {"query_string": {"query": "v"}}),
        (q.ElasticQueryString(), {"query_string": {"query": "*"}}),
        (q.ElasticTermQuery(field="f", value="v"), {"term": {"f": "v"}}),
        (q.ElasticTermQuery(field="f", value='"v"'), {"term": {"f": "v"}}),
        (q.ElasticFuzzyQuery(field="f", value="v"), {"fuzzy": {"f": "v"}}),
        (q.ElasticFuzzyQuery(field="f", value='"v"'), {"fuzzy": {"f": "v"}}),
        (q.ElasticExistsQuery(field="f"), {"exists": {"field": "f"}}),
        (q.ElasticFullMatchQuery(field="f", value="v"), {"match_phrase": {"f": "v"}}),
        (q.ElasticFullMatchQuery(field="f", value="v", boosting=1), {"match_phrase": {"f": "v", "boosting": 1}}),
        (q.ElasticFullMatchQuery(field="f", value='"v"'), {"match_phrase": {"f": "v"}}),
        (q.ElasticMatchQuery(field="f", value="v"), {"match": {"f": "v"}}),
        (q.ElasticMatchQuery(field="f", value="v", boosting=1), {"match": {"f": "v", "boosting": 1}}),
        (q.ElasticMatchQuery(field="f", value='"v"'), {"match": {"f": "v"}}),
        (q.ElasticRangeQuery(field="f", value_from=0, value_to=1), {"range": {"f": {"gte": 0, "lte": 1}}}),
        (q.ElasticRangeQuery(field="f", value_from=1, value_to=0), {"range": {"f": {"gte": 0, "lte": 1}}}),
        (q.ElasticGeoPointRangeQuery(field="f", value_from="[2, 3]", value_to="[3, 4]"), {"geo_bounding_box": {"location.coordinates": {"bottom_right": {"lat": "3", "lon": " 4"}, "top_left": {"lat": "2", "lon": " 3"}}}}),
        (q.ElasticGeoPointQuery(field="f", value="[1,1]"), {"geo_bounding_box": {"location.coordinates": {"bottom_right": {"lat": "1", "lon": "1"}, "top_left": {"lat": "1", "lon": "1"}}}}),
        (q.ElasticNestedQuery(query=q.ElasticExistsQuery(field="f"), nested_path="core"), {"nested": {"path": "core", "query": {"exists": {"field": "f"}}}})
    ],
)
def test_query_writing(auto_query, query):
    assert auto_query.get_query() == query

@pytest.mark.parametrize(
    "query",
    [
        q.ElasticQueryString(),
        q.ElasticTermQuery(field="f", value="v"),
        q.ElasticFuzzyQuery(field="f", value="v"),
        q.ElasticExistsQuery(field="f"),
        q.ElasticFullMatchQuery(field="f", value="v"),
        q.ElasticMatchQuery(field="f", value="v"),
        q.ElasticRangeQuery(field="f", value_from=0, value_to=1),
        q.ElasticGeoPointRangeQuery(field="f", value_from="[2, 3]", value_to="[3, 4]"),
        q.ElasticGeoPointQuery(field="f", value="[1,1]"),
        q.ElasticNestedQuery(query=q.ElasticExistsQuery(field="f"), nested_path="core")
    ],
)
def test_query_bool(query):
    hardcode_and = q.ElasticBoolMust(queries=[query, query])
    hardcode_or = q.ElasticBoolShould(queries=[query, query])

    auto_and = query & query
    assert auto_and.get_query() == hardcode_and.get_query()

    auto_rand = query
    auto_rand &= query
    assert auto_and.get_query() == hardcode_and.get_query()

    auto_or = query | query
    assert auto_or.get_query() == hardcode_or.get_query()

    auto_ror = query
    auto_ror |= query
    assert auto_ror.get_query() == hardcode_or.get_query()

