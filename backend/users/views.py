from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from .models import User
from .serializers import PasswordChangeSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False, url_path='me', methods=['GET'])
    def get_current_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, url_path='set_password', methods=['POST'])
    def set_password(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=HTTP_204_NO_CONTENT)
