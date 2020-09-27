from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api_recipes.models import Recipe, Step, Food, Ingredient, User
from api_recipes.serializers import RecipeSerializer, StepSerializer, FoodSerializer, IngredientSerializer, \
    UserSerializer


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


class UserViewSet(CustomModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    http_method_names = ['post', 'head', 'patch', 'options', 'delete']
