from elasticsearch_tools import query as q

query_string = q.generate_query(_type="query_string", field="f", value="v")
print(query_string.get_query())
# {"query_string": {"default_field": "f", "query": "v"}}

term = q.generate_query(_type="term", field="f", value="v")
print(term.get_query())
# {"term": {"f": "v"}}

fuzzy = q.generate_query(_type="fuzzy", field="f", value="v")
print(fuzzy.get_query())
# {"fuzzy": {"f": "v"}}

exists = q.generate_query(_type="exists", field="f")
print(exists.get_query())
# {"exists": {"field": "f"}}

match_phrase = q.generate_query(_type="match_phrase", field="f", value="v", boosting=1)
print(match_phrase.get_query())
# {"match_phrase": {"f": "v", "boosting": 1}}

match = q.generate_query(_type="match", field="f", value="v", boosting=1)
print(match.get_query())
# {"match": {"f": "v", "boosting": 1}}

_range = q.generate_query(_type="range", field="f", value_from=0, value_to=1)
print(_range.get_query())
# {"range": {"f": {"gte": 0, "lte": 1}}}

geo_bounding_box = q.generate_query(_type="geo_point_range", field="f", value_from="[2, 3]", value_to="[3, 4]")
print(geo_bounding_box.get_query())
# {"geo_bounding_box": {"location.coordinates": {"bottom_right": {"lat": "3", "lon": " 4"}, "top_left": {"lat": "2", "lon": " 3"}}}}

geo_bounding_box_2 = q.generate_query(_type="geo_point", field="f", value="[1,1]")
print(geo_bounding_box_2.get_query())
# {"geo_bounding_box": {"location.coordinates": {"bottom_right": {"lat": "1", "lon": "1"}, "top_left": {"lat": "1", "lon": "1"}}}}

