from django_user_agents.utils import get_user_agent
from django.contrib.sessions.backends.db import SessionStore

from .models import (
    Device,
    Browser,
    OS
)

from .serializers import ClientSerializer

def get_device_obj(device):
    return Device.objects.get_or_create(
        brand=device.brand,
        family=device.family,
        model=device.model
    )[0]

def get_browser_obj(browser):
    return Browser.objects.get_or_create(
        family=browser.family,
        version=browser.version_string
    )[0]

def get_os_obj(os):
    return OS.objects.get_or_create(
        family=os.family,
        version=os.version_string
    )[0]

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def insert_client_session(request,user):
    """ 
    Creating Session Information 
    Take a look at https://docs.djangoproject.com/en/2.2/_modules/django/contrib/auth/
    """
    session = SessionStore()
    session['_auth_user_id'] = user.id
    session['_auth_user_hash'] = user.get_session_auth_hash()
    session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
    session.create()

    """ Setting Client Informations """
    user_agent = get_user_agent(request)

    client_data = {
        'session' : session.session_key,
        'user' : user.id,
        'device':get_device_obj(user_agent.device).id,
        'browser':get_browser_obj(user_agent.browser).id,
        'os':get_os_obj(user_agent.os).id,
        'ua_string':user_agent.ua_string,
        'ip':get_client_ip(request),
    }
    client_session_serializer = ClientSerializer(data=client_data)
    if client_session_serializer.is_valid(raise_exception=True):
        client_session = client_session_serializer.save()
    
    return client_session
