from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'phone']

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)

        user.set_password(password)
        user.role = CustomUser.SELLER
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'account_type', 'phone', 'is_verified']
        read_only_fields = ['id', 'account_type', 'is_verified']


class ManagerCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone']

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.role = CustomUser.MANAGER
        user.is_verified = True
        user.is_staff = True
        user.account_type = 'premium'

        user.save()
        return user