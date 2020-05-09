from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.views import APIView

from rest_framework.authtoken.models import Token

from .models import (
    User,
    UserKey
)
from .serializers import (
    BaseUserSerializer,
    BaseActivateUserSerializer,
    BaseResetPWUserSerializer,
)

class OutsideUserViews(APIView):
    def get(self, request, method):
        if method == 'activate':
            return self.__activate_user(request)
        if method == 'password_forgotten':
            return self.__password_forgotten(request)

        return self.__wrong_method(request)

    def post(self, request, method):
        if method == 'create':
            return self.__create_user(request)
        if method == 'reset_password':
            return self.__reset_password(request)

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

        data = {
            'user':user_serializer.data,
            'token':Token.objects.get(user=new_user).key
        }

        return Response(data, status=status.HTTP_201_CREATED)

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

    def __password_forgotten(self,request):
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
