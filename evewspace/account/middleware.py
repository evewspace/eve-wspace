from django.contrib.auth import logout

class StrictAuthentication(object):
    def process_view(self, request, *args, **kwargs):
        if request.user.is_authenticated() and not request.user.is_active:
            logout(request)
