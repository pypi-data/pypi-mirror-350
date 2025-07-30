import pytest

from elasticsearch_tools import query as q


@pytest.mark.parametrize(
    "query, function_kwargs",
    [
        (q.ElasticQueryString(field="f", value="v"), {"_type": "query_string", "field": "f", "value": "v"}),
        (q.ElasticQueryString(field="f"), {"_type": "query_string", "field": "f"}),
        (q.ElasticQueryString(value="v"), {"_type": "query_string", "value": "v"}),
        (q.ElasticQueryString(), {"_type": "query_string"}),
        (q.ElasticTermQuery(field="f", value="v"), {"_type": "term", "field": "f", "value": "v"}),
        (q.ElasticTermQuery(field="f", value='"v"'), {"_type": "term", "field": "f", "value": '"v"'}),
        (q.ElasticFuzzyQuery(field="f", value="v"), {"_type": "fuzzy", "field": "f", "value": '"v"'}),
        (q.ElasticFuzzyQuery(field="f", value='"v"'), {"_type": "fuzzy", "field": "f", "value": "v"}),
        (q.ElasticExistsQuery(field="f"), {"_type": "exists", "field": "f"}),
        (q.ElasticFullMatchQuery(field="f", value="v"), {"_type": "match_phrase", "field": "f", "value": "v"}),
        (q.ElasticFullMatchQuery(field="f", value="v", boosting=1), {"_type": "match_phrase", "field": "f", "value": "v", "boosting": 1}),
        (q.ElasticMatchQuery(field="f", value="v"), {"_type": "match", "field": "f", "value": "v"}),
        (q.ElasticMatchQuery(field="f", value="v", boosting=1), {"_type": "match", "field": "f", "value": "v", "boosting": 1}),
        (q.ElasticRangeQuery(field="f", value_from=0, value_to=1), {"_type": "range", "field": "f", "value_from": 0, "value_to": 1}),
        (q.ElasticGeoPointRangeQuery(field="f", value_from="[2, 3]", value_to="[3, 4]"), {"_type": "geo_point_range", "field": "f", "value_from": "[2, 3]", "value_to": "[3, 4]"}),
        (q.ElasticGeoPointQuery(field="f", value="[1,1]"), {"_type": "geo_point", "field": "f", "value": "[1,1]"}),
    ],
)
def test_query_writing(query, function_kwargs):
    new_query = q.generate_query(**function_kwargs)
    assert new_query.get_query() == query.get_query()
