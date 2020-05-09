from django.urls import path,include

urlpatterns = [
    path(
        'auth/',
        include('User.User.urls'),
    ),
]
