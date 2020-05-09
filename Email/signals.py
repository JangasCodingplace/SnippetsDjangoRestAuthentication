from django.dispatch import receiver

from django.conf import settings

from django.db.models.signals import (
    post_save,
    pre_save
)

from User.User.models import (
    UserKey,
    User
)

from . import email

@receiver(post_save, sender=UserKey)
def send_activation_mail(*args, **kwargs):
    if kwargs['created']:
        key = kwargs['instance']
        if key.key_type == 'a':
            if settings.ENV['SEND_ACTIVATION_MAIL'] == 'False':
                return
            email.send_message(
                message=key.get_activation_message(),
                receiver=key.user.email,
                subject='Activate your Account!'
            )
        if key.key_type == 'pw':
            if settings.ENV['SEND_PASSWORD_FORGOTTEN_MAIL'] == 'False':
                return
            email.send_message(
                message=key.get_pw_reset_message(),
                receiver=key.user.email,
                subject='Password Reset Link'
            )

@receiver(pre_save, sender=User)
def send_email_change_mail(*args, **kwargs):
    user = kwargs['instance']
    if user:
        old_email = User.objects.get(pk=user.pk).email
        if user.email != old_email:
            if settings.ENV['SEND_EMAIL_CHANGE_NOTIFICATION_MAIL'] == 'False':
                return
            email.send_message(
                message=user.get_email_change_mail(),
                receiver=old_email,
                subject='Your Email has changed'
            )
