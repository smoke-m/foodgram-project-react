from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.mixins import CreateListRetrieveViewSet
from .models import Follow, User
from .serializers import (FollowSerializer, PasswordChangeSerializer,
                          UserCreteSerializer, UserSerializer)


class UserViewSet(CreateListRetrieveViewSet):
    """Вьюсет модели User."""
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ('create',):
            return UserCreteSerializer
        return UserSerializer

    @action(detail=False, url_path='me', methods=('get',),
            permission_classes=(permissions.IsAuthenticated,))
    def get_current_user(self, request):
        """Метод 'me'."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, url_path='set_password', methods=('post',),
            permission_classes=(permissions.IsAuthenticated,))
    def set_password(self, request):
        """Метод 'set_password'."""
        serializer = PasswordChangeSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, url_path='subscribe', methods=('post', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, pk):
        """Метод создания и удаления 'subscribe'."""
        user = request.user
        author = get_object_or_404(User, id=pk)
        change_subscription_status = Follow.objects.filter(
            user=user.id, author=author.id)
        if request.method == 'POST':
            if user == author:
                return Response({'errors': 'Нельзя подписаться на себя!'},
                                status=status.HTTP_400_BAD_REQUEST)
            if change_subscription_status.exists():
                return Response({'errors': 'Уже подписаны!'},
                                status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=user, author=author).save()
            serializer = FollowSerializer(
                author, context={'request': request},)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if change_subscription_status.exists():
            change_subscription_status.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Такой подписки нет'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path='subscriptions', methods=('get',),
            permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        """Метод получения списка 'subscriptions'."""
        queryset = User.objects.filter(follow__user=self.request.user)
        if queryset:
            queryset_pag = self.paginate_queryset(queryset)
            serializer = FollowSerializer(
                queryset_pag, context={'request': request}, many=True,)
            return self.get_paginated_response(serializer.data)
        return Response({'errors': 'Подписок нет'},
                        status=status.HTTP_400_BAD_REQUEST)
