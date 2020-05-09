from django.dispatch import receiver

from django.db.models.signals import (
    post_save,
)

from User.User.models import User
from .models import UserKey

@receiver(post_save, sender=User)
def create_token(*args, **kwargs):
    if kwargs['created']:
        UserKey.objects.create(
            user=kwargs['instance'],
            key_type='a'
        )
