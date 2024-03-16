from rest_framework import serializers

from apps.accounts.models import User, GateManager, CheckInManager


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True,
    )
    user_permissions = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True
    )
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)


    class Meta:
        model = User
        exclude = ["password"]


class BaseManagerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(source="user.password")

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return user


class CheckInManagerSerializer(BaseManagerSerializer):
    class Meta:
        model = CheckInManager
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        check_in_manager = CheckInManager.objects.create(user=user)
        return check_in_manager


class GateManagerSerializer(BaseManagerSerializer):
    class Meta:
        model = GateManager
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        gate_manager = GateManager.objects.create(user=user)
        return gate_manager
