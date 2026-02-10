from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class RefreshViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
