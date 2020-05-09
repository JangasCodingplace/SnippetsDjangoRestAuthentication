from django.urls import path

from . import api

urlpatterns = [
    path(
        '<slug:method>',
        api.UserKeyViews.as_view(),
        name='APIUserKeyViews'
    )
]
