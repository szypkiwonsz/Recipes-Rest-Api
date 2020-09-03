from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Recipe
from .serializers import RecipeSerializer


class IsAuthenticatedOrGet(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return super(IsAuthenticatedOrGet, self).has_permission(request, view)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrGet]
