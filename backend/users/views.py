from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowSerializer, UserSerializer


class UserViewSet(DjoserUserViewSet):
    """Вьюсет модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, url_path='subscribe', methods=('post', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, id):
        """Метод создания и удаления 'subscribe'."""
        user = request.user
        author = get_object_or_404(User, id=id)
        change_subscription_status = Follow.objects.filter(
            user=user.id, author=author.id)
        if request.method == 'POST':
            if change_subscription_status.exists():
                return Response({'detail': 'Уже подписаны!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FollowSerializer(
                author, context={'request': request},
                data={'user': user.id, 'author': author.id}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author).save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if change_subscription_status.exists():
            change_subscription_status.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Такой подписки нет'},
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
        return Response({'detail': 'Подписок нет'},
                        status=status.HTTP_400_BAD_REQUEST)
