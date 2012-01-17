from django.conf import settings

KEY = getattr(settings, 'AUTOMATIC_LOGIN_KEY', 'mtkn')
