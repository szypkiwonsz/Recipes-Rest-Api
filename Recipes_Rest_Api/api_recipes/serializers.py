from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin

from .models import Recipe, Ingredient, Food, Step


class FoodSerializer(UniqueFieldsMixin, serializers.ModelSerializer):

    def create(self, validated_data):
        obj, created = Food.objects.get_or_create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        return super(FoodSerializer, self).update(instance, validated_data)

    class Meta:
        model = Food
        fields = '__all__'


class StepSerializer(UniqueFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Step
        fields = '__all__'


class IngredientSerializer(WritableNestedModelSerializer):
    food = FoodSerializer()

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(WritableNestedModelSerializer):
    ingredients = IngredientSerializer(many=True)
    steps = StepSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'
