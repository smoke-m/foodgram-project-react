from django.urls import include, path
from rest_framework import routers
from djoser import views as djoser_views
from djoser.urls import authtoken

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
