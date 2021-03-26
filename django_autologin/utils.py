from six.moves.urllib import parse as urlparse

from django.conf import settings
from django.contrib import auth
from django.core.signing import TimestampSigner, BadSignature

from . import app_settings

SEPARATOR = ':'

def get_automatic_login_token(user):
    signer = TimestampSigner(salt=get_user_salt(user), sep=SEPARATOR)
    return signer.sign(user.pk)


def validate_token(user, token, max_age=None) -> bool:
    if SEPARATOR not in token:
        return False

    if max_age is None:
        max_age = app_settings.MAX_AGE

    try:
        signer = TimestampSigner(salt=get_user_salt(user), sep=SEPARATOR)
        user_id = signer.unsign(token, max_age=max_age)
        return user_id == str(user.id)
    except BadSignature:
        return False


def strip_token(url):
    bits = urlparse.urlparse(url)
    original_query = urlparse.parse_qsl(bits.query)

    query = [(k, v) for k, v in original_query if k != app_settings.KEY]

    query = urlparse.urlencode(query)

    return urlparse.urlunparse((bits[0], bits[1], bits[2], bits[3], query, bits[5]),)


def login(request, user):
    user.backend = settings.AUTHENTICATION_BACKENDS[0]
    auth.login(request, user)


def get_user_salt(user):
    parts = []

    for field in app_settings.SALT_FIELDS:
        # Follow "django__join__notation'
        part = user
        for x in field.split("__"):
            part = getattr(part, x)

        parts.append(part)

    return "".join(str(x) for x in parts)
