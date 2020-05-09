from django.dispatch import receiver

from django.db.models.signals import (
    post_save,
)

from rest_framework.authtoken.models import Token
from .models import (
    User,
    UserKey
)

@receiver(post_save, sender=User)
def create_token(*args, **kwargs):
    if kwargs['created']:
        Token.objects.create(
            user=kwargs['instance']
        )

@receiver(post_save, sender=User)
def create_access_key(*args, **kwargs):
    if kwargs['created']:
        UserKey.objects.create(
            user=kwargs['instance'],
            key_type='a'
        )
