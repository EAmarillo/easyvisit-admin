from rest_framework import serializers
from .models import UrbanizationManagers


class UrbanizationManagersSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=48)
    last_name = serializers.CharField(max_length=48)
    phone = serializers.IntegerField(max_value=9999999999)
    email = serializers.EmailField(max_length=64)
    is_active = serializers.BooleanField(required=False, default=True)
    urbanization = serializers.IntegerField()

    class Meta:
        model = UrbanizationManagers
        fields = ('__all__')
