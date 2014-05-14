from cdf.log import logger


def get_urlid(visit_stream_entry,
              url_to_id,
              urlid_to_http_code):
    """Find the url id corresponding to an entry in a visit stream.
    The function checks if the http and https version of the url exist.
    (ie pages have been crawled)
    If only one of them exists, it returns the corresponding url id.
    If none exist, it returns None.
    If both exist, it returns https id if the http is a redirection
    and http id in all other case.
    :param visit_stream_entry: an entry from the visit stream.
    :type visit_stream_entry: list
    :param url_to_id: the dict url -> urlid
    :type url_to_id: dict
    :param urlid_to_http_code: a dict urlid -> http code
    :type urlid_to_http_code: dic
    :returns: int
    """
    url = visit_stream_entry[0]
    #generate candidate url ids
    candidates = []
    for protocol in ["http", "https"]:
        candidate_url = '{}://{}'.format(protocol, url)
        url_id = url_to_id.get(candidate_url, None)
        if url_id is None:
            continue
        candidates.append((protocol, url_id))

    def has_been_crawled(url_id, urlid_to_http_code):
        http_code = urlid_to_http_code.get(url_id, None)
        if http_code is None:
            return False
        #do not consider urls that have not been crawled
        if http_code == 0:
            return False
        return True

    #remove candidates that have not been crawled
    candidates = [(protocol, urlid) for protocol, urlid in candidates if
                  has_been_crawled(urlid, urlid_to_http_code)]

    #make a decision
    if len(candidates) == 0:
        return None
    elif len(candidates) == 1:
        protocol, urlid = candidates[0]
        return urlid
    elif len(candidates) == 2:
        protocol_to_urlid = {protocol: urlid for protocol, urlid in candidates}
        https_urlid = protocol_to_urlid["https"]
        http_urlid = protocol_to_urlid["http"]
        http_code = urlid_to_http_code.get(http_urlid, None)
        if 300 <= http_code and http_code < 400:
            return https_urlid
        else:
            return http_urlid
    return None
