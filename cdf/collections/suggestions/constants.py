from cdf.streams.mapping import CONTENT_TYPE_INDEX


CROSS_PROPERTIES_COLUMNS = ('query', 'content_type', 'depth', 'http_code', 'index', 'follow')

COUNTERS_FIELDS = (
    'pages_nb',
    'total_delay_ms',
    'redirects_to_nb',
    'redirects_from_nb',
    'canonical_nb',
    'canonical_nb.filled',
    'canonical_nb.not_filled',
    'canonical_nb.equal',
    'canonical_nb.not_equal',
    'canonical_nb.incoming',

    'inlinks_internal_nb',
    'inlinks_internal_nb.total',
    'inlinks_internal_nb.total_unique',
    'inlinks_internal_nb.follow',
    'inlinks_internal_nb.follow_unique',
    'inlinks_internal_nb.nofollow',
    'inlinks_internal_nb.nofollow_combinations',
    'inlinks_internal_nb.nofollow_combinations.link',
    'inlinks_internal_nb.nofollow_combinations.link_meta',
    'inlinks_internal_nb.nofollow_combinations.link_meta_robots',
    'inlinks_internal_nb.nofollow_combinations.link_robots',
    'inlinks_internal_nb.nofollow_combinations.meta',
    'inlinks_internal_nb.nofollow_combinations.meta_robots',

    'inlinks_internal_nb.follow_distribution_urls.1',
    'inlinks_internal_nb.follow_distribution_urls.2',
    'inlinks_internal_nb.follow_distribution_urls.3',
    'inlinks_internal_nb.follow_distribution_urls.4',
    'inlinks_internal_nb.follow_distribution_urls.5',
    'inlinks_internal_nb.follow_distribution_urls.6',
    'inlinks_internal_nb.follow_distribution_urls.7',
    'inlinks_internal_nb.follow_distribution_urls.8',
    'inlinks_internal_nb.follow_distribution_urls.9',
    'inlinks_internal_nb.follow_distribution_urls.lte_3',
    'inlinks_internal_nb.follow_distribution_urls.lt_10',
    'inlinks_internal_nb.follow_distribution_urls.10_to_19',
    'inlinks_internal_nb.follow_distribution_urls.20_to_29',
    'inlinks_internal_nb.follow_distribution_urls.30_to_39',
    'inlinks_internal_nb.follow_distribution_urls.40_to_49',
    'inlinks_internal_nb.follow_distribution_urls.50_to_99',
    'inlinks_internal_nb.follow_distribution_urls.100_to_999',
    'inlinks_internal_nb.follow_distribution_urls.1000_to_9999',
    'inlinks_internal_nb.follow_distribution_urls.10000_to_99999',
    'inlinks_internal_nb.follow_distribution_urls.100000_to_999999',
    'inlinks_internal_nb.follow_distribution_urls.gte_1M',

    'inlinks_internal_nb.follow_distribution_links.1',
    'inlinks_internal_nb.follow_distribution_links.2',
    'inlinks_internal_nb.follow_distribution_links.3',
    'inlinks_internal_nb.follow_distribution_links.4',
    'inlinks_internal_nb.follow_distribution_links.5',
    'inlinks_internal_nb.follow_distribution_links.6',
    'inlinks_internal_nb.follow_distribution_links.7',
    'inlinks_internal_nb.follow_distribution_links.8',
    'inlinks_internal_nb.follow_distribution_links.9',
    'inlinks_internal_nb.follow_distribution_links.lte_3',
    'inlinks_internal_nb.follow_distribution_links.lt_10',
    'inlinks_internal_nb.follow_distribution_links.10_to_19',
    'inlinks_internal_nb.follow_distribution_links.20_to_29',
    'inlinks_internal_nb.follow_distribution_links.30_to_39',
    'inlinks_internal_nb.follow_distribution_links.40_to_49',
    'inlinks_internal_nb.follow_distribution_links.50_to_99',
    'inlinks_internal_nb.follow_distribution_links.100_to_999',
    'inlinks_internal_nb.follow_distribution_links.1000_to_9999',
    'inlinks_internal_nb.follow_distribution_links.10000_to_99999',
    'inlinks_internal_nb.follow_distribution_links.100000_to_999999',
    'inlinks_internal_nb.follow_distribution_links.gte_1M',

    'outlinks_internal_nb',
    'outlinks_internal_nb.total',
    'outlinks_internal_nb.total_unique',
    'outlinks_internal_nb.follow',
    'outlinks_internal_nb.follow_unique',
    'outlinks_internal_nb.nofollow',
    'outlinks_internal_nb.nofollow_combinations',
    'outlinks_internal_nb.nofollow_combinations.link',
    'outlinks_internal_nb.nofollow_combinations.link_meta',
    'outlinks_internal_nb.nofollow_combinations.link_meta_robots',
    'outlinks_internal_nb.nofollow_combinations.link_robots',
    'outlinks_internal_nb.nofollow_combinations.meta',
    'outlinks_internal_nb.nofollow_combinations.meta_robots',
    'outlinks_internal_nb.nofollow_combinations.robots',

    'outlinks_external_nb',
    'outlinks_external_nb.total',
    'outlinks_external_nb.follow',
    'outlinks_external_nb.nofollow',
    'outlinks_external_nb.nofollow_combinations',
    'outlinks_external_nb.nofollow_combinations.link',
    'outlinks_external_nb.nofollow_combinations.link_meta',
    'outlinks_external_nb.nofollow_combinations.meta',

    'delay_gte_2s',
    'delay_from_1s_to_2s',
    'delay_from_500ms_to_1s',
    'delay_lt_500ms',
    'metadata_nb',
    'metadata_nb.not_enough',

    'error_links.3xx',
    'error_links.4xx',
    'error_links.5xx',
    'error_links.any'
)

for ct_txt in CONTENT_TYPE_INDEX.itervalues():
    COUNTERS_FIELDS += ('metadata_nb.%s.not_filled' % ct_txt, 'metadata_nb.%s.filled' % ct_txt, 'metadata_nb.%s.unique' % ct_txt, 'metadata_nb.%s.duplicate' % ct_txt)
