from rest_framework import serializers
from .models import Account
from rest_framework.validators import UniqueValidator


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "following",
            "copies",
            "is_colaborator",
            "is_superuser",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "following",
            "copies",
            "is_superuser",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=Account.objects.all(),
                        message="A user with that email already exists.",
                    )
                ]
            },
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=Account.objects.all(),
                        message="A user with that username already exists.",
                    )
                ],
                "write_only": True,
                "required": True,
            },
            "first_name": {"required": True},
            "last_name": {"required": True},
            "is_colaborator": {"allow_null": True, "default": False},
        }

        depth = 0

    def validate(self, attrs: dict):
        is_colab = attrs.get("is_colaborator", None)

        if is_colab:
            attrs["is_superuser"] = True

        return attrs

    def create(self, validated_data: dict):
        if validated_data.get("is_superuser", None):
            return Account.objects.create_superuser(**validated_data)

        return Account.objects.create_user(**validated_data)

    def update(self, instance: Account, validated_data: dict):
        instance.email = validated_data.get("email", instance.email)

        new_password = validated_data.get("password", None)
        if new_password:
            instance.password = instance.set_password(new_password)

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        instance.save()

        return instance
