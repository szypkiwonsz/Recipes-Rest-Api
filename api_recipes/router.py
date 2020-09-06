from rest_framework import routers

from .views import RecipeViewSet, FoodViewSet, StepViewSet, IngredientViewSet

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('foods', FoodViewSet, basename='food')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('steps', StepViewSet, basename='steep')
