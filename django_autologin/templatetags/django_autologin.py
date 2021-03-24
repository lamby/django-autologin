from django import template

from .. import app_settings
from ..utils import get_automatic_login_token

register = template.Library()


@register.simple_tag
def automatic_login_token(user):
    token = get_automatic_login_token(user)

    return "%s=%s" % (app_settings.KEY, token)
