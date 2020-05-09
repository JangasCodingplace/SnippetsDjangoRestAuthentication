import uuid
import os

from django.utils.timezone import now
from datetime import timedelta

from django.conf import settings
from django.db import models

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

from django.utils.timezone import now

KEY_TYPE = [
    ('pw', 'Password Forgotten'),
    ('a', 'Activation'),
    ('auth', 'Authentication'),
]

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise AttributeError('Users must have an email address')
        if not first_name:
            raise AttributeError('Users must have a first_name')
        if not last_name:
            raise AttributeError('Users must have an last_name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.activation_date = now()
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    first_name = models.CharField(
        max_length=60
    )
    last_name = models.CharField(
        max_length=60
    )
    is_active = models.BooleanField(
        default=False
    )
    is_admin = models.BooleanField(
        default=False
    )
    registration_date = models.DateTimeField(
        auto_now_add=True
    )
    first_activation_date = models.DateTimeField(
        blank=True,
        null=True,
        editable=False
    )
    previous_version = None
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    @property
    def full_name(self):
        return f"{self.last_name}, {self.first_name}"


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def get_email_change_mail(self):
        mail_template_path = os.path.join(
            settings.BASE_DIR,
            'User',
            'User',
            'templates',
            'mails',
            'email_change_notification.html'
        )

        mail_template = open(mail_template_path, 'r')
        body = mail_template.read()
        mail_template.close()
        body = body.replace(
            '{{USER}}',
            self.first_name
        )
        return body

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

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
        max_length=4,
        choices=KEY_TYPE,
    )

    @property
    def is_valid(self):
        if self.key_type == 'a':
            period_time = int(settings.ENV['ACTIVATION_KEY_PERIODS_OF_VALIDITY'])
        elif self.key_type == 'auth':
            period_time = int(settings.ENV['ACCES_KEY_PERIODS_OF_VALIDITY'])
        else:
            period_time = int(settings.ENV['PASSWORD_KEY_PERIODS_OF_VALIDITY'])
        limit_time = self.creation_time + timedelta(minutes=period_time)
        return now() < limit_time

    def get_activation_message(self):
        mail_template_path = os.path.join(
            settings.BASE_DIR,
            'User',
            'User',
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
        body = body.replace(
            '{{USER}}',
            self.user.first_name
        )
        body = body.replace(
            '{{ACTIVATION_KEY}}',
            activation_link
        )
        return body

    def get_pw_reset_message(self):
        mail_template_path = os.path.join(
            settings.BASE_DIR,
            'User',
            'User',
            'templates',
            'mails',
            'password_forgotten.html'
        )
        mail_template = open(mail_template_path, 'r')
        body = mail_template.read()
        mail_template.close()
        reset_link = "{}{}?key={}".format(
            settings.ENV['FRONTEND_URL'],
            settings.ENV['FRONTEND_ACCOUNT_PASSWORD_FORGOTTEN_URL'],
            self.key
        )
        body = body.replace(
            '{{USER}}',
            self.user.first_name
        )
        body = body.replace(
            '{{KEY_CREATION_TIME}}',
            self.creation_time.strftime("%m.%d.%Y, %H:%M:%S")
        )
        body = body.replace(
            '{{PW_RESET_LINK}}',
            reset_link
        )

        return body

    def __str__(self):
        return f'{self.key} ({self.key_type})'

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.key_type == 'a':
                if self.user.is_active:
                    raise AttributeError('An active User can not have an validation key.')

            else:
                if not self.user.is_active:
                    raise ValueError('A not activated User can not get Access by Email or Reset Password.')
                UserKey.objects.filter(user=self.user).delete()

            self.key = uuid.uuid4().hex[:8]
            while UserKey.objects.filter(key=self.key).exists():
                self.key = uuid.uuid4().hex[:8]

        super().save(*args, **kwargs)
