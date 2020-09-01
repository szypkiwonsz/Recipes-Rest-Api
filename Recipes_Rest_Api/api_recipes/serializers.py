from rest_framework import serializers

from .models import Recipe, Ingredient, Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    food = FoodSerializer()

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            # foods_data must be a list, because there is one field in the database
            foods_data = [ingredient_data.pop('food')]
            for food_data in foods_data:
                food, created = Food.objects.get_or_create(**food_data)
                ingredient_data, _ = Ingredient.objects.get_or_create(food_id=food.pk, **ingredient_data)
                recipe.ingredients.add(ingredient_data)
        return recipe
