from django.contrib.auth import authenticate
from rest_framework import serializers

from flujopay_backend_test.app_users.models import User
from flujopay_backend_test.utils.customs_serializers import BaseSerializer
from flujopay_backend_test.utils.simple_functions import get_tokens_jwt


class LoginSerializer(BaseSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def _validate_credentials(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()
        if not user:
            raise ValueError({"email": ["El correo no existe"]})

        user = authenticate(username=email, password=password)
        if not user:
            raise ValueError({"password": ["La contraseña es incorrecta"]})

        self.context["user"] = user

    def get_tokens(self, obj):
        user = self.context["user"]
        return get_tokens_jwt(user, 1, 7)
