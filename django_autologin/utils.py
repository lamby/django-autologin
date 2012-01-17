import urllib
import urlparse

from . import app_settings

def strip_token(url):
    bits = urlparse.urlparse(url)
    original_query = urlparse.parse_qsl(bits.query)

    query = {}
    for k, v in original_query:
        if k != app_settings.KEY:
            query[k] = v

    query = urllib.urlencode(query)

    return urlparse.urlunparse(
        (bits[0], bits[1], bits[2], bits[3], query, bits[5]),
    )
