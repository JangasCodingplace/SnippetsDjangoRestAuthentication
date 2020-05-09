from django.urls import path, include

urlpatterns = [
    path(
        'auth/',
        include('User.User.urls'),
    ),
    path(
        '',
        include('User.Key.urls'),
    )
]
