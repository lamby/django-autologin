import urllib
import urlparse

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.cache import add_never_cache_headers
from django.contrib.auth import login
from django.core.signing import TimestampSigner, BadSignature
from django.contrib.auth.models import User

class AutomaticLoginMiddleware(object):
    def __init__(self):
        try:
            self.key = settings.AUTOMATIC_LOGIN_KEY
        except AttributeError:
            self.key = 'mtkn'

    def strip_token(self, url):
        bits = urlparse.urlparse(url)
        original_query = urlparse.parse_qsl(bits.query)

        query = {}
        for k, v in original_query:
            if k != self.key:
                query[k] = v

        query = urllib.urlencode(query)

        return urlparse.urlunparse(
            (bits[0], bits[1], bits[2], bits[3], query, bits[5]),
        )

    def process_request(self, request):
        if request.user.is_authenticated():
            return

        token = request.GET.get(self.key)
        if not token:
            return

        user_id = token.split(':', 1)[0]

        try:
            user = User.objects.get(id=user_id)
        except (ValueError, User.DoesNotExist):
            return redirect(self.strip_token(request.get_full_path()))

        try:
           TimestampSigner(salt=user.password).unsign(
                token, max_age=60*60*24*90,
            )
        except BadSignature:
            return redirect(self.strip_token(request.get_full_path()))

        if request.method == 'POST':
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user)
            return HttpResponse()

        response = render(request, 'account/auto_login_redirect.html', {
            'path': self.strip_token(request.get_full_path()),
            'token': token,
        })

        add_never_cache_headers(response)

        return response
