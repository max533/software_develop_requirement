from django.conf import settings
from django.contrib.auth import login
from django.http.response import JsonResponse
from django.views.decorators.csrf import requires_csrf_token

from .models import CustomUser


@requires_csrf_token
def force_login(request):
    """ Provide force_login feature with POSTMAN API Tool when DEBUG=TRUE """
    username = settings.DJANGO_FORCE_LOGIN_USERNAME
    user = CustomUser.objects.filter(username=username).first()
    data = dict()
    if not user:
        data['message'] = 'Please login with CAS first, then you cas use this feature.'
        return JsonResponse(data)
    login(request, user, backend=settings.AUTHENTICATION_BACKENDS[1])
    data['message'] = f"Login Successfully with user <{username}>"
    return JsonResponse(data)
