from django import template
from django.core.signing import TimestampSigner

from .. import app_settings
from ..utils import get_user_salt

register = template.Library()

@register.simple_tag
def automatic_login_token(user):
    token = TimestampSigner(
        salt=get_user_salt(user),
    ).sign(user.pk)

    return "%s=%s" % (app_settings.KEY, token)
