from django import template
from django.core.signing import TimestampSigner

from .. import app_settings, utils

register = template.Library()

@register.simple_tag
def automatic_login_token(user):
    token = TimestampSigner(
        salt=utils.get_user_salt(user),
    ).sign(user.id)

    return "%s=%s" % (app_settings.KEY, token)
