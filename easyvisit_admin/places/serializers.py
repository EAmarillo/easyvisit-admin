from rest_framework import serializers
from .models import Place


class PlaceSerializers(serializers.ModelSerializer):
    street = serializers.CharField(max_length=48)
    number = serializers.CharField(max_length=8)
    neighborhood = serializers.CharField(max_length=32)
    city = serializers.CharField(max_length=16)
    state = serializers.CharField(max_length=16)
    country = serializers.CharField(max_length=16)
    zip_code = serializers.IntegerField(max_value=99999)
    is_active = serializers.BooleanField(required=False, default=True)
    urbanization = serializers.IntegerField
    description = serializers.CharField(max_length=200,
                                        allow_null=True,
                                        required=False)

    class Meta:
        model = Place
        fields = ('__all__')
