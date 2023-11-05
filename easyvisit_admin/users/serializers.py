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
    first_name = serializers.CharField(max_length=48)
    last_name = serializers.CharField(max_length=48)
    email = serializers.EmailField(max_length=64)
    is_active = serializers.BooleanField(required=False, default=True)
    place = serializers.IntegerField
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)

    class Meta:
        model = APIUser
        fields = ('__all__')


class UploadCSVSerializer(serializers.Serializer):
    csv_file = serializers.FileField(
        allow_empty_file=False,
        allow_null=False,
        use_url=False
    )

    def validate_csv_file(self, file):
        if not file.name.endswith('.csv'):
            raise serializers.ValidationError('The file must be in CSV format.')

        max_csv_size = 10 * 1024 * 1024
        if file.size > max_csv_size:
            raise serializers.ValidationError('The file is too large. The maximum allowed size is 10 MB.')

        return file
