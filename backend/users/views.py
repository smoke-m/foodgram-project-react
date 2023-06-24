from djoser.views import UserViewSet
from rest_framework import generics


class UserView(generics.RetrieveAPIView):
    serializer_class = UserViewSet.serializer_class

    def get_object(self):
        return self.request.user
