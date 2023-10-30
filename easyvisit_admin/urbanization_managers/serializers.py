from rest_framework import serializers
from .models import UrbanizationManager


class UrbanizationManagersSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=48)
    last_name = serializers.CharField(max_length=48)
    phone = serializers.IntegerField(max_value=9999999999, min_value=1000000000)
    email = serializers.EmailField(max_length=64)
    is_active = serializers.BooleanField(required=False, default=True)
    urbanization = serializers.IntegerField

    class Meta:
        model = UrbanizationManager
        fields = ('__all__')
