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
                food, _ = Food.objects.get_or_create(**food_data)
                ingredient_data, _ = Ingredient.objects.get_or_create(food_id=food.pk, **ingredient_data)
                recipe.ingredients.add(ingredient_data)
        return recipe

    def update(self, instance, validated_data):
        try:
            ingredients_data = validated_data.pop('ingredients')
        except KeyError:
            ingredients_data = []
        instance = super(RecipeSerializer, self).update(instance, validated_data)
        for ingredient_data in ingredients_data:
            foods_data = [ingredient_data.pop('food')]
            for food_data in foods_data:
                food_qs = Food.objects.filter(
                    name__iexact=food_data['name']
                )

                if food_qs.exists():
                    food = food_qs.first()
                else:
                    food = Food.objects.create(**food_data)

                ingredient_qs = Ingredient.objects.filter(
                    unit__iexact=ingredient_data['unit']).filter(
                    amount__iexact=ingredient_data['amount']).filter(food_id=food.pk)

                if ingredient_qs.exists():
                    ingredient = ingredient_qs.first()
                else:
                    ingredient = Ingredient.objects.create(food_id=food.pk, **ingredient_data)

                instance.ingredients.add(ingredient)

        return instance
