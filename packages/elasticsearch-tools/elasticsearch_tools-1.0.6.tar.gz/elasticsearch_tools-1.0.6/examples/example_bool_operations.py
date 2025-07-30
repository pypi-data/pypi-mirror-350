from elasticsearch_tools import query as q

# Negation
# May be interesting

must_query = q.ElasticBoolMust([])
must_not_query = q.ElasticBoolMustNot([])
negate_must = ~must_query
assert must_not_query.get_query() == negate_must.get_query()

# Bool operations

query = q.ElasticQueryString()
query_2 = q.ElasticExistsQuery(field="f")

# OR operation
should_query = query | query_2
assert should_query.get_query() == {"bool": {"should": [{"query_string": {"default_field": "*", "query": "*"}}, {"exists": {"field": "f"}}]}}

# AND operation

must_query = query & query_2
assert must_query.get_query() == {"bool": {"must": [{"query_string": {"default_field": "*", "query": "*"}}, {"exists": {"field": "f"}}]}}
