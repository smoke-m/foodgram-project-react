from rest_framework import generics
from djoser.views import UserViewSet

class UserView(generics.RetrieveAPIView):
    serializer_class = UserViewSet.serializer_class

    def get_object(self):
        return self.request.user
