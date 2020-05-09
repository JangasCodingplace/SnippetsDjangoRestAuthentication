from django.dispatch import receiver

from django.conf import settings

from django.db.models.signals import (
    post_save,
)

from User.User.models import UserKey

from . import email

@receiver(post_save, sender=UserKey)
def send_activation_mail(*args, **kwargs):
    if settings.ENV['SEND_ACTIVATION_MAIL'] == 'False':
        return
    if kwargs['created']:
        key = kwargs['instance']
        if not key.user.is_active:
            email.send_message(
                message=key.get_activation_message(),
                receiver=key.user.email,
                subject='Activate your Account!'
            )
