from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.cache import add_never_cache_headers
from django.contrib.auth import login
from django.core.signing import TimestampSigner, BadSignature
from django.contrib.auth.models import User

from . import app_settings
from .utils import strip_token

class AutomaticLoginMiddleware(object):
    def process_request(self, request):
        token = request.GET.get(app_settings.KEY)
        if not token:
            return

        try:
            user_id = int(token.split(':', 1)[0])

            # Only change user if necessary.
            if request.user.id == user_id:
                return

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
