from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken

from api_recipes.views import RecipeViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', ObtainAuthToken.as_view(), name='auth')
]
