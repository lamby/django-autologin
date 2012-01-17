from django import template
from django.conf import settings
from django.core.signing import TimestampSigner

register = template.Library()

@register.simple_tag
def automatic_login_token(user):
    try:
        key = settings.AUTOMATIC_LOGIN_KEY
    except AttributeError:
        key = 'mtkn'

    token = TimestampSigner(
        salt=user.password,
    ).sign(user.id)

    return "%s=%s" % (key, token)
