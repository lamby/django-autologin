from django.conf import settings

KEY = getattr(settings, 'AUTOMATIC_LOGIN_KEY', 'mtkn')
MAX_AGE = getattr(settings, 'AUTOMATIC_LOGIN_MAX_AGE', 60 * 60 * 24 * 90)
SALT_FIELDS = getattr(settings, 'AUTOMATIC_LOGIN_SALT_FIELDS', ('password',))
