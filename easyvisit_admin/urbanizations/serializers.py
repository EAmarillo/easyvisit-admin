from rest_framework import serializers
from .models import Urbanization, Plan


class UrbanizationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=48)
    street = serializers.CharField(max_length=48)
    number = serializers.CharField(max_length=8)
    neighborhood = serializers.CharField(max_length=32)
    city = serializers.CharField(max_length=16)
    state = serializers.CharField(max_length=16)
    country = serializers.CharField(max_length=16)
    zip_code = serializers.IntegerField(max_value=99999)
    houses = serializers.IntegerField(max_value=999999)
    is_active = serializers.BooleanField(required=False, default=True)
    rfc = serializers.CharField(min_length=13, max_length=13, required=False, default='XXXX000000X00')
    email = serializers.EmailField(max_length=64)
    plan = serializers.IntegerField

    class Meta:
        model = Urbanization
        fields = ('__all__')


class PlanSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=10)
    price = serializers.FloatField()

    class Meta:
        model = Plan
        fields = ('__all__')
