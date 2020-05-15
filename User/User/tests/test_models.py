from datetime import timedelta

from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIRequestFactory

from django.utils.timezone import now

from rest_framework.authtoken.models import Token
from User.User.models import (
    User,
    UserKey
)

class UserModelTest(TestCase):
    """ User and UserKey get texted in this class """
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email='root@admin.de',
            first_name='root',
            last_name='admin',
            password='rootpassword',
        )
        self.user = User.objects.create_user(
            email='user@admin.de',
            first_name='user',
            last_name='admin',
            password='rootpassword',
        )

    def test_admin_is_active(self):
        assert self.superuser.is_active and self.superuser.is_admin

    def test_user_is_not_active(self):
        assert not self.user.is_active

    def test_if_token_got_generated(self):
        assert Token.objects.filter(
            user=self.superuser
        ).exists()
        assert Token.objects.filter(
            user=self.user
        ).exists()

    def test_if_user_activation_key_exists(self):
        assert UserKey.objects.filter(
            user=self.user,
            key_type='a'
        ).exists()

    def test_activation_key_is_valid(self):
        key = UserKey.objects.get(
            user=self.user,
            key_type='a'
        )

        creation_time = key.creation_time
        period_time = int(settings.ENV['ACTIVATION_KEY_PERIODS_OF_VALIDITY'])

        key.creation_time = creation_time - timedelta(minutes=period_time - 1)
        key.save()
        assert key.is_valid

    def test_activation_key_is_not_valid(self):
        key = UserKey.objects.get(
            user=self.user,
            key_type='a'
        )

        creation_time = key.creation_time
        period_time = int(settings.ENV['ACTIVATION_KEY_PERIODS_OF_VALIDITY'])

        key.creation_time = creation_time - timedelta(minutes=period_time + 1)
        key.save()

        assert not key.is_valid
    def test_only_one_valid_key_per_user(self):
        pass    
    def test_no_password_reset_for_not_active_user(self):
        pass
    def test_no_tmp_for_not_active_user(self):
        pass
    def test_pw_reset_key_is_valid(self):
        pass
    def test_pw_reset_key_is_not_valid(self):
        pass
    def test_auth_key_is_valid(self):
        pass
    def test_auth_key_is_not_valid(self):
        pass
    def test_activation_key_gets_remove_by_manual_activation(self):
        pass
    def test_user_activation_message(self):
        pass
    def test_user_pw_forgotten_message(self):
        pass
    def test_email_has_changed_message(self):
        pass
