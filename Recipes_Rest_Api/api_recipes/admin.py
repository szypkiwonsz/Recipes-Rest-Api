from django.contrib import admin
from api_recipes.models import Recipe, Ingredient, Food


# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Food)
