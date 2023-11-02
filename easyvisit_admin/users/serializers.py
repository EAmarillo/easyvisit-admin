from rest_framework import serializers
from .models import Role, APIUser


class RoleSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=16)
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = Role
        fields = ('__all__')


class APIUserSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(max_value=9999999999, min_value=1000000000)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(max_length=48)
    last_name = serializers.CharField(max_length=48)
    email = serializers.EmailField(max_length=64)
    is_active = serializers.BooleanField(required=False, default=True)
    place = serializers.IntegerField
    role = serializers.IntegerField

    class Meta:
        model = APIUser
        fields = ('__all__')
