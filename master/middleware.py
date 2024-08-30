from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.contrib.auth import login

class AlwaysLoggedInMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            # Replace 'default_user_username' with the username of the default user
            default_user = get_user_model().objects.get(username='play')
            login(request, default_user)