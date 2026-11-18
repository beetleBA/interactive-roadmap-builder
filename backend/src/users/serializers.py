from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

from .models import Stack, UserStack
from .services.avatar import prepare_avatar
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()


class AvatarMixin:
    def validate_avatar(self, value):
        try:
            return prepare_avatar(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages) from exc


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'date_joined',
            'avatar',
            'bio'
        ]
        read_only_fields = fields


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            self.context.get('request'),
            username=username,
            password=password,
        )
        if user is None:
            raise serializers.ValidationError('Неверный логин или пароль.')

        attrs['user'] = user
        return attrs


class RegisterSerializer(AvatarMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'avatar',
            'password',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UpdateSerializer(AvatarMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'avatar',
            'bio',
        )


class StackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = '__all__'


class UserStackSerializer(serializers.ModelSerializer):
    stack = StackSerializer(read_only=True)
    stack_id = serializers.PrimaryKeyRelatedField(
        source="stack",
        queryset=Stack.objects.all(),
        write_only=True,
    )

    class Meta:
        model = UserStack
        fields = ("id", "stack", "stack_id")
        read_only_fields = ("id", "stack")

    def validate(self, attrs):
        user = self.context["request"].user
        stack = attrs.get("stack")

        if stack is not None:
            queryset = UserStack.objects.filter(
                user=user,
                stack=stack,
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError({
                    "stack_id": "Такая технология уже добавлена в профиль."
                })

        return attrs
