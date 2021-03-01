from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

from api_recipes.models import Recipe, Step, Food, Ingredient, User
from api_recipes.serializers import RecipeSerializer, StepSerializer, FoodSerializer, IngredientSerializer, \
    UserSerializer


class IsOwnerOrGet(BasePermission):
    """
    The inheriting class needed for authorization of an object (edit and detail page).

    UNAUTHORIZED -> GET
    AUTHORIZED (NOT AUTHOR) -> GET
    AUTHENTICATED (AUTHOR) -> ALL
    SUPERUSER -> ALL
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.author == request.user


class IsAuthenticatedOrGet(IsAuthenticated):
    """
    The inheriting class needed for authentication of ViewSet.

    UNAUTHENTICATED -> GET
    AUTHENTICATED -> GET, POST
    SUPERUSER -> ALL
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return super(IsAuthenticatedOrGet, self).has_permission(request, view)


class CustomModelViewSet(viewsets.ModelViewSet):
    """Custom model view set for our view sets."""
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']
    authentication_classes = [TokenAuthentication]


class RecipeViewSet(CustomModelViewSet):
    """Inheriting recipe view set with filtering by author."""
    queryset = Recipe.objects.all().order_by('-date_posted')
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrGet, IsOwnerOrGet]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class StepViewSet(CustomModelViewSet):
    """Inheriting step view set."""
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = [IsAuthenticated]


class FoodViewSet(CustomModelViewSet):
    """Inheriting food view set."""
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]


class IngredientViewSet(CustomModelViewSet):
    """Inheriting ingredient view set."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(CustomModelViewSet):
    """Inheriting user view set."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'head', 'patch', 'options', 'delete']
