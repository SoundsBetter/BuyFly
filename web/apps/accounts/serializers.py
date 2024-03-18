from rest_framework import serializers

from .models import User, GateManager, CheckInManager


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True,
    )

    class Meta:
        model = User
        exclude = ["password"]
        read_only_fields = ["is_active", "is_staff", "is_superuser"]


class BaseManagerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    password = serializers.CharField(source="user.password", read_only=True)

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
