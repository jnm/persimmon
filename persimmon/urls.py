"""persimmon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
import threading

from django.conf import settings
from django.contrib import admin, auth
from django.http import HttpResponse
from django.urls import include, path

from oidc_provider import views as oidc_views


def oops(request, *args, **kwargs):
    return HttpResponse(
        '<html><body>'
        f'<p>Hello, {request.user}.</p>'
        "<p>I'm just an authentication provider. You probably meant to go to "
        'an application that connects with me.</p>'
        "<p>If you'd like to change your password, "
        '<a href="/accounts/password_change">click here</a>.</p>'
        "<p>If you're trying to administer users, go to "
        '<a href="/admin/">/admin/</a>.</p>'
        '</body></html>',
        content_type='text/html'
    )

def authorize_wrapper(request, *args, **kwargs):
    if settings.LOGOUT_SECONDS_AFTER_OIDC_AUTHORIZE > 0:
        threading.Timer(
            settings.LOGOUT_SECONDS_AFTER_OIDC_AUTHORIZE,
            lambda: auth.logout(request),
        ).start()
    return oidc_views.AuthorizeView.as_view()(request, *args, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('openid/authorize', authorize_wrapper, name='authorize'),
    path('openid/authorize/', authorize_wrapper, name='authorize'),
    path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    path('accounts/profile/', oops),
    path('', oops),
]
