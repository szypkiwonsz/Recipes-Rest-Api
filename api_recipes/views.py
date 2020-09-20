from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .models import Recipe, Step, Food, Ingredient
from .serializers import RecipeSerializer, StepSerializer, FoodSerializer, IngredientSerializer


class IsAuthenticatedOrGet(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return super(IsAuthenticatedOrGet, self).has_permission(request, view)


class CustomModelViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']
    authentication_classes = [TokenAuthentication]


class RecipeViewSet(CustomModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrGet]
    parser_classes = [FormParser, MultiPartParser]


class StepViewSet(CustomModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = [IsAuthenticated]


class FoodViewSet(CustomModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]


class IngredientViewSet(CustomModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]
