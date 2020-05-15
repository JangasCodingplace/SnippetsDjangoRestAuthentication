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
            'password',
            'is_active',
        )

        extra_kwargs = {
            'password':{
                'write_only':True
            },
            'is_active':{
                'read_only':True
            }
        }

    def create(self, validated_data):
        """Creates New User"""
        return User.objects.create(**validated_data)

class BaseUserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name',
            'email',
            'is_active'
        )

        extra_kwargs = {
            'is_active':{
                'read_only':True,
            },
            'first_name':{
                'required':False
            },
            'last_name':{
                'required':False
            },
            'email':{
                'required':False
            },
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name',
            instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name',
            instance.last_name
        )
        instance.email = validated_data.get(
            'email',
            instance.email
        )
        instance.save()
        return instance

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


