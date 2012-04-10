import urllib
import urlparse

from django.conf import settings
from django.contrib import auth

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

def login(request, user):
    user.backend = settings.AUTHENTICATION_BACKENDS[0]
    auth.login(request, user)

def get_user_salt(user):
    return "".join(str(getattr(user, x)) for x in app_settings.SALT_FIELDS)
