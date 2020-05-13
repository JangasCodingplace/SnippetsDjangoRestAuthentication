from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import (
    User,
    UserKey
)
from .serializers import (
    BaseUserSerializer,
    BaseActivateUserSerializer,
    BaseResetPWUserSerializer,
    BaseUserChangeSerializer,
    OpenSessionSerializer
)

class OutsideUserViews(APIView):
    def get(self, request, method):
        if method == 'activate':
            return self.__activate_user(request)
        if method == 'password_forgotten':
            return self.__password_forgotten(request)
        if method == 'get_user_by_key':
            return self.__get_user_by_key(request)

        return self.__wrong_method(request)

    def post(self, request, method):
        if method == 'create':
            return self.__create_user(request)
        if method == 'reset_password':
            return self.__reset_password(request)
        if method == 'authentication':
            return self.__authentication(request)

        return self.__wrong_method(request)

    def __wrong_method(self, request):
        data = {
            'err':'Wrong or missing URL Method',
        }

        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def __create_user(self, request):
        if User.objects.filter(email=request.data['email']).exists():
            data = {
                'err':'User with that Email does already exist.'
            }
            return Response(data, status=status.HTTP_409_CONFLICT)

        user_serializer = BaseUserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            new_user = user_serializer.save()
        
        open_session_serializer = OpenSessionSerializer(
            data={'user':new_user.id}
        )
        if open_session_serializer.is_valid(raise_exception=True):
            open_session = open_session_serializer.save()

        data = {
            'user':user_serializer.data,
            'token':Token.objects.get(user=new_user).key,
            'session':open_session.key
        }

        return Response(data, status=status.HTTP_201_CREATED)

    def __authentication(self, request):
        user = authenticate(
            request,
            email=request.data['email'],
            password=request.data['password']
        )
        if user is None:
            data = {
                'err':'User does not exist or wrong password.'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        user_serializer = BaseUserSerializer(user)
        
        open_session_serializer = OpenSessionSerializer(
            data={'user':user.id}
        )
        if open_session_serializer.is_valid(raise_exception=True):
            open_session = open_session_serializer.save()

        data = {
            'user':user_serializer.data,
            'token':Token.objects.get(user=user).key,
            'session':open_session.key
        }
        return Response(data, status=status.HTTP_200_OK)

    def __reset_password(self, request):
        try:
            key = UserKey.objects.get(
                key=request.data['key'],
                key_type='pw'
            )
        except UserKey.DoesNotExist:
            data = {
                'err':'invalid key.'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        if not key.is_valid:
            data = {
                'err':'key out of validity period'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        user_serializer = BaseResetPWUserSerializer(key.user, request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            key.delete()

        data = {
            'user':user_serializer.data,
            'token':Token.objects.get(user=user).key
        }

        return Response(data, status=status.HTTP_200_OK)

    def __get_user_by_key(self, request):
        """ Only for already activated Users """
        key = request.data['key']
        try:
            key = UserKey.objects.get(key=key)
        except UserKey.DoesNotExist:
            data = {
                'err':'invalid key.'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if not key.is_valid:
            data = {
                'err':'key out of validity period'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        if key.key_type == 'a':
            data = {
                'err':'Wrong Keytype.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = BaseUserSerializer(key.user)
        key.delete()

        data = {
            'user':user_serializer.data,
            'token':Token.objects.get(user=key.user).key
        }

        return Response(data, status=status.HTTP_200_OK)

    def __activate_user(self, request):
        key = request.data['key']
        try:
            key = UserKey.objects.get(key=key)
        except UserKey.DoesNotExist:
            data = {
                'err':'invalid key.'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if not key.is_valid:
            data = {
                'err':'key out of validity period'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        user_serializer = BaseActivateUserSerializer(key.user, data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            key.delete()

        data = {
            'user':user_serializer.data,
            'token':Token.objects.get(user=user).key
        }

        return Response(data, status=status.HTTP_202_ACCEPTED)

    def __password_forgotten(self, request):
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            data = {
                'err':'User with that Email does already exist.'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        data = {
            'user':user.id,
            'key_type':'pw',
        }
        UserKey.objects.create(
            user=user,
            key_type='pw'
        )

        data = {
            'msg':'Email was sended to given Email.'
        }

        return Response(data, status=status.HTTP_200_OK)

class UserViwes(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, method):
        if method == 'change_password':
            return self.__change_password(request)
        if method == 'update_user_infos':
            return self.__update_user_infos(request)

        return self.__wrong_method(request)

    def __wrong_method(self, request):
        data = {
            'err':'Wrong or missing URL Method',
        }

        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def __change_password(self, request):
        user_serializer = BaseResetPWUserSerializer(request.user, request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()

        data = {
            'user':user_serializer.data,
            'token':Token.objects.get(user=user).key
        }

        return Response(data, status=status.HTTP_200_OK)

    def __update_user_infos(self, request):
        user_serializer = BaseUserChangeSerializer(request.user, data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
        data = {
            'user':user_serializer.data,
            'token':Token.objects.get(user=user).key
        }
        return Response(data, status=status.HTTP_200_OK)
