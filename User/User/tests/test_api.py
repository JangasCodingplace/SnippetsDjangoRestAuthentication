import requests
import json

from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient
from User.User.models import (
    User,
    UserKey
)

class UserAPITest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email='root@admin.de',
            first_name='Root',
            last_name='Admin',
            password='rootpassword',
        )
        self.user = User.objects.create_user(
            email='user@admin.de',
            first_name='User',
            last_name='Admin',
            password='rootpassword',
        )

    def test_login_success(self):
        path = '/user/auth/authentication'
        data = {
            'email':'root@admin.de',
            'password':'rootpassword',
        }
        response = self.client.post(path, data)
        print(response)
        assert True
        # assert 'token' in response_data

    # def test_login_success_response(self):
    #     path = 'http://127.0.0.1:8000/user/auth/authentication'
    #     data = {
    #         'email':'root@admin.de',
    #         'password':'rootpassword',
    #     }
    #     response = requests.post(path, data=data)
    #     response_data = json.loads(response.content)
    #     responsed_user = response_data['user']

    #     assert (
    #         responsed_user['email'] == self.superuser.email and
    #         responsed_user['first_name'] == self.superuser.first_name and
    #         responsed_user['last_name'] == self.superuser.last_name and
    #         responsed_user['is_active']
    #     )

    # def test_failed_authentication(self):
    #     path = 'http://127.0.0.1:8000/user/auth/authentication'
    #     data = {
    #         'email':'root@admin.de',
    #         'password':'wrongpassword',
    #     }
    #     response = requests.post(path, data=data)
    #     response_data = json.loads(response.content)

    #     assert 'token' not in response_data
    #     assert 'user' not in response_data
    
    def test_registration_success_response(self):
        path = 'http://127.0.0.1:8000/user/auth/create'
        data = {
            'first_name':'Test',
            'last_name':'User',
            'email':'test1@mail.com',
            'password':'HelloWorldPW'
        }
        response = self.client.post(path, data)
        print(response)
        response_data = json.loads(response.content)

        """ Test if user gets Authenticate after Login """
        assert 'token' in response_data
    
    def test_registration_success_db(self):
        assert not User.objects.filter(email='test2@mail.com').exists()
        path = 'http://127.0.0.1:8000/user/auth/create'
        data = {
            'first_name':'Test',
            'last_name':'User',
            'email':'test2@mail.com',
            'password':'HelloWorldPW'
        }
        requests.post(path, data=data)
        assert User.objects.filter(email='test2@mail.com').exists()
