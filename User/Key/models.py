import uuid
import os

from django.utils.timezone import now
from datetime import timedelta

from django.db import models

from django.conf import settings

KEY_TYPE = [
    ('pw', 'Password Forgotten'),
    ('a', 'activation'),
]

class UserKey(models.Model):
    key = models.CharField(
        primary_key=True,
        max_length=8,
        editable=False
    )
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='users_key'
    )
    creation_time = models.DateTimeField(
        auto_now_add=True
    )
    key_type = models.CharField(
        max_length=2,
        choices=KEY_TYPE,
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = uuid.uuid4().hex[:8]
            while UserKey.objects.filter(key=self.key).exists():
                self.key = uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)

    @property
    def key_is_valid(self):
        if self.key_type == 'a':
            period_time = int(settings.ENV['ACTIVATION_KEY_PERIODS_OF_VALIDITY'])
        else:
            period_time = int(settings.ENV['PASSWORD_KEY_PERIODS_OF_VALIDITY'])
        limit_time = self.creation_time + timedelta(minutes=period_time)
        return now() < limit_time

    def get_activation_message(self):
        mail_template_path = os.path.join(
            settings.BASE_DIR,
            'User',
            'Key',
            'templates',
            'mails',
            'activation.html'
        )

        mail_template = open(mail_template_path, 'r')
        body = mail_template.read()
        mail_template.close()
        activation_link = "{}{}?key={}".format(
            settings.ENV['FRONTEND_URL'],
            settings.ENV['FRONTEND_ACCOUNT_ACTIVATION_URL'],
            self.key
        )
        body = body.replace('{{USER}}', self.user.first_name)
        body = body.replace('{{ACTIVATION_KEY}}', activation_link)
        return body
