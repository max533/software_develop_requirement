"""develop_requirement_dev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django_cas_ng.views

from develop_requirement_proj.signature.views import (
    DownloadView, IndexView, NotificationView,
)

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('cas/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('cas/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('cas/callback', django_cas_ng.views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
    path('download/<int:order_id>/<str:filename>/', DownloadView.as_view(), name='download'),
    path('notification/', NotificationView.as_view(), name='notification')
]


# API URLS
urlpatterns += [
    path("api/", include("config.api_router")),
]

if settings.DEBUG:
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view

    from rest_framework import permissions

    schema_view = get_schema_view(
        openapi.Info(
            title='Auto Order Planner',
            default_version='v1',
            description='',
        ),
        public=True,
        permission_classes=(permissions.IsAuthenticated,),
    )

    # Force Login feature path
    urlpatterns += [
        path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
        path('users/', include("develop_requirement_proj.users.urls"))
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
