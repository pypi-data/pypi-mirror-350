# elasticsearch-tools

*Made with official Python client for Elasticsearch, [elasticsearch-py](https://github.com/elastic/elasticsearch-py/)*


## Features

* Translating basic Python data types to and from JSON
* Configurable automatic discovery of cluster nodes
* Persistent connections
* Load balancing (with pluggable selection strategy) across available nodes
* Failed connection penalization (time based - failed connections won't be
  retried until a timeout is reached)
* Support for TLS and HTTP authentication
* Thread safety across requests
* Pluggable architecture
* Helper functions for idiomatically using APIs together
* Native connection object for sync and async sessions
* Connection object for dependency in Fastapi, or async generators
* Helper functions for query writing from code

## Usage elasticsearch-py
-----

* [Creating an index](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_creating_an_index)
* [Indexing a document](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_indexing_documents)
* [Getting documents](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_getting_documents)
* [Searching documents](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_searching_documents)
* [Updating documents](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_updating_documents)
* [Deleting documents](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_deleting_documents)
* [Deleting an index](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_deleting_an_index)


## Environment variables:
* field_pattern - regex for validate field, if you need
* default_nested_path - path for nested fields, if dont add to args to init

## Query types

| Class object              | name for generate_query | Official |
|---------------------------|-------------------------|----------|
| ElasticQueryString        | query_string            | yes      |
| ElasticTermQuery          | term                    | yes      |
| ElasticFuzzyQuery         | fuzzy                   | yes      |
| ElasticExistsQuery        | exists                  | yes      |
| ElasticFullMatchQuery     | match_phrase            | yes      |
| ElasticMatchQuery         | match                   | yes      |
| ElasticRangeQuery         | range                   | yes      |
| ElasticGeoPointRangeQuery | geo_point_range         | yes      |
| ElasticGeoPointQuery      | geo_point               | no       |
| ElasticNestedQuery        | nested                  | yes      |

## Official documentation

Documentation for the client is [available on elastic.co] and [Read the Docs].

[available on elastic.co]: https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
[Read the Docs]: https://elasticsearch-py.readthedocs.io

## License

This software is licensed under the [Apache License 2.0](./LICENSE). See [NOTICE](./NOTICE).

## Deploy

Update dist

```shell
python3.9 setup.py sdist
```

Upload dist

```shell
twine upload dist/*
```

