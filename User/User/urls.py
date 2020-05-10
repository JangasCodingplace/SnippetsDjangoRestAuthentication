from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import api

urlpatterns = [
    path(
        'auth/<slug:method>',
        api.OutsideUserViews.as_view(),
        name='APIUserOutsideViews'
    ),
    path(
        '<slug:method>',
        api.UserViwes.as_view(),
        name='APIUserViews',
    ),
    path(
        'login/',
        obtain_auth_token,
        name="APILogin"
    )
]
