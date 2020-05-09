from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.views import APIView

from rest_framework.authtoken.models import Token

from .models import User
from .serializers import BaseUserSerializer

class OutsideUserViews(APIView):
    def post(self, request, method):
        if method == 'create':
            return self.create_user(request)

        data = {
            'err':'Wrong or missing URL Method',
        }

        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def create_user(self, request):
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
