from django.dispatch import receiver

from django.db.models.signals import (
    post_save,
)

from User.User.models import User

from . import email

@receiver(post_save, sender=User)
def send_activation_mail(*args, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        email.send_message(
            message=user.get_activation_message(),
            receiver=user.email,
            subject='Activate your Account!'
        )
