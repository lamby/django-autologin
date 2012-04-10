from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers
from django.core.signing import TimestampSigner, BadSignature
from django.contrib.auth.models import User

from . import app_settings
from .utils import login, strip_token, get_user_salt

class AutomaticLoginMiddleware(object):
    def process_request(self, request):
        token = request.GET.get(app_settings.KEY)
        if not token:
            return

        r = redirect(strip_token(request.get_full_path()))

        try:
            pk = int(token.split(':', 1)[0])

            # Only change user if necessary. We strip the token in any case.
            # The AnonymousUser class has no 'pk' attribute (#18093)
            if getattr(request.user, 'pk', request.user.id) == pk:
                return r

            user = User.objects.get(pk=pk)
        except (ValueError, User.DoesNotExist):
            return r

        try:
            TimestampSigner(salt=get_user_salt(user)).unsign(
                token, max_age=app_settings.MAX_AGE,
            )
        except BadSignature:
            return r

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
