from django import template

from ..utils import get_automatic_login_token

register = template.Library()
register.simple_tag(get_automatic_login_token, name="automatic_login_token")
