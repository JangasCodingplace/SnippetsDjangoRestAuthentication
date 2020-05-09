from rest_framework import serializers

from .models import User

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password':{
                'write_only':True,
            },
        }

    def create(self, validated_data):
        return User.objects.create(**validated_data)
