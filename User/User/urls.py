from django.urls import path

from . import api

urlpatterns = [
    path(
        '<slug:method>',
        api.OutsideUserViews.as_view(),
        name='APIUserOutsideViews'
    ),
]
