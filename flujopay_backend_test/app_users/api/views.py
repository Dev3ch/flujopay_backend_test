from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from flujopay_backend_test.app_users.api.serializers import LoginSerializer


class AuthViewSet(viewsets.GenericViewSet, TokenRefreshView):
    @action(detail=False, methods=["POST"], url_path="login")
    def login(self, request: Request) -> Response:
        serializer = LoginSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], url_path="refresh-token")
    def refresh(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
