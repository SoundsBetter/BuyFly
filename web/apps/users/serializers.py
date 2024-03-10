from django.contrib.auth.models import Group
from rest_framework import serializers

from apps.users.apis import CheckInManager
from apps.users.models import User, GateManager


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail')
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


class BaseManagerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedIdentityField(
        read_only=True, view_name='user-detail'
    )
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


class GateManagerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GateManager
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        gate_manager = GateManager.objects.create(user=user)
        return gate_manager
