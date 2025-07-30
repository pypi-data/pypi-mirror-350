from elasticsearch_tools import query as q

query_string = q.ElasticQueryString(field="f", value="v")
print(query_string.get_query())
# {"query_string": {"default_field": "f", "query": "v"}}

term = q.ElasticTermQuery(field="f", value="v")
print(term.get_query())
# {"term": {"f": "v"}}

fuzzy = q.ElasticFuzzyQuery(field="f", value="v")
print(fuzzy.get_query())
# {"fuzzy": {"f": "v"}}

exists = q.ElasticExistsQuery(field="f")
print(exists.get_query())
# {"exists": {"field": "f"}}

match_phrase = q.ElasticFullMatchQuery(field="f", value="v", boosting=1)
print(match_phrase.get_query())
# {"match_phrase": {"f": "v", "boosting": 1}}

match = q.ElasticMatchQuery(field="f", value="v", boosting=1)
print(match.get_query())
# {"match": {"f": "v", "boosting": 1}}

_range = q.ElasticRangeQuery(field="f", value_from=0, value_to=1)
print(_range.get_query())
# {"range": {"f": {"gte": 0, "lte": 1}}}

geo_bounding_box = q.ElasticGeoPointRangeQuery(field="f", value_from="[2, 3]", value_to="[3, 4]")
print(geo_bounding_box.get_query())
# {"geo_bounding_box": {"location.coordinates": {"bottom_right": {"lat": "3", "lon": " 4"}, "top_left": {"lat": "2", "lon": " 3"}}}}

geo_bounding_box_2 = q.ElasticGeoPointQuery(field="f", value="[1,1]")
print(geo_bounding_box_2.get_query())
# {"geo_bounding_box": {"location.coordinates": {"bottom_right": {"lat": "1", "lon": "1"}, "top_left": {"lat": "1", "lon": "1"}}}}

nested = q.ElasticNestedQuery(query=q.ElasticExistsQuery(field="f"), nested_path="core")
print(nested.get_query())
# {"nested": {"path": "core", "query": {"exists": {"field": "f"}}}}
