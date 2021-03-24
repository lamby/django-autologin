from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

from . import app_settings
from .utils import login, strip_token, validate_token

User = get_user_model()


class AutomaticLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.GET.get(app_settings.KEY)
        if not token:
            return

        r = redirect(strip_token(request.get_full_path()))

        try:
            pk = int(token.split(":", 1)[0])

            # Only change user if necessary. We strip the token in any case.
            # The AnonymousUser class has no 'pk' attribute (#18093)
            if getattr(request.user, "pk", request.user.id) == pk:
                return r

            user = User.objects.get(pk=pk)
        except (ValueError, User.DoesNotExist):
            return r

        if not validate_token(user, token):
            return r

        response = self.render(
            request, user, token, strip_token(request.get_full_path()),
        )

        add_never_cache_headers(response)

        return response

    def render(self, request, user, token, path):
        """
        Subclasses may override this behaviour.
        """

        login(request, user)

        return redirect(path)
