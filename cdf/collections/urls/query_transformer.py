from copy import deepcopy

from cdf.collections.urls.query_parsing import parse_botify_query


__ALL__ = ['get_es_query']


def _merge_filters(query, filters):
    """Merge filters to botify query using `and` filter

    New filters are places BEFORE the original filters.

    :param query: the botify format query
    :param filters: a list of botify predicate to merge
    :return: the extended query
    """
    botify_query = deepcopy(query)
    to_merge = deepcopy(filters)

    if not 'filters' in botify_query:
        botify_query['filters'] = {'and': to_merge}
        return botify_query

    # try to merge into existing, outer `and` filter
    if 'and' in botify_query['filters']:
        botify_query['filters']['and'] = filters + botify_query['filters']['and']
        return botify_query

    # create a new `and` filter for merging
    to_merge.append(botify_query['filters'])
    botify_query['filters'] = {'and': to_merge}
    return botify_query


def get_es_query(botify_query, crawl_id):
    """Generate ElasticSearch query from a botify query

    :param botify_query: a botify query generated by front-end
    :param crawl_id: unique id of the crawl in question
    :returns: a valid ElasticSearch query, in json format
    """

    # By default all queries should have these filter/predicate
    #   1. only query for current crawl/site
    #   2. only query for urls whose http_code != 0 (crawled urls)
    # The order is important for and/or/not filters in ElasticSearch
    # See: http://www.elasticsearch.org/blog/all-about-elasticsearch-filter-bitsets/
    default_filters = [
        {'field': 'crawl_id', 'value': crawl_id},
        {'not': {'field': 'http_code', 'value': 0, 'predicate': 'eq'}}
    ]

    # Merge default filters in botify format query
    botify_query = _merge_filters(botify_query, default_filters)

    return parse_botify_query(botify_query).transform()