from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers
from django.core.signing import TimestampSigner, BadSignature
from django.contrib.auth.models import User

from . import app_settings
from .utils import login, strip_token

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
            return redirect(strip_token(request.get_full_path()))

        try:
            TimestampSigner(salt=user.password).unsign(
                token, max_age=60*60*24*90,
            )
        except BadSignature:
            return redirect(strip_token(request.get_full_path()))

        response = self.render(
            request,
            user,
            token,
            strip_token(request.get_full_path()),
        )

        add_never_cache_headers(response)

        return response

    def render(self, request, user, token, path):
        """
        Subclasses may override this behaviour.
        """

        login(request, user)

        return redirect(path)
