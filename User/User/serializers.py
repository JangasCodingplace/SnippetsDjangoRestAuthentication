from rest_framework import serializers

from .models import (
    User,
    UserKey
)

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name',
            'email',
            'is_active',
            'password'
        )

        extra_kwargs = {
            'password':{
                'write_only':True,
            },
        }

    def create(self, validated_data):
        """Creates New User"""
        return User.objects.create(**validated_data)


class BaseActivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'is_active'
        )
        read_only_fields = (
            'first_name',
            'last_name',
            'email'
        )

    def update(self, instance, validated_data):
        """Handles just Account activation"""
        instance.is_active = True
        instance.save()
        return instance

class BaseResetPWUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'is_active',
            'password'
        )
        read_only_fields = (
            'first_name',
            'last_name',
            'is_active',
            'email'
        )
        extra_kwargs = {
            'password':{
                'write_only':True,
            },
        }

    def update(self, instance, validated_data):
        """
            Handles just PW Reset
        """
        print(validated_data['password'])
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
