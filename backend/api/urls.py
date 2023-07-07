from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UsersViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='djoser_views')
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
