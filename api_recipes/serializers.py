from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin
from rest_framework import serializers

from api_recipes.models import Recipe, Ingredient, Food, Step, User


class FoodSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    """Food serializer."""

    def create(self, validated_data):
        obj, created = Food.objects.get_or_create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        return super(FoodSerializer, self).update(instance, validated_data)

    class Meta:
        model = Food
        fields = '__all__'


class StepSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    """Recipe step serializer."""

    class Meta:
        model = Step
        fields = '__all__'


class IngredientSerializer(WritableNestedModelSerializer):
    """Food ingredient serializer."""
    food = FoodSerializer()

    class Meta:
        model = Ingredient
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}, 'required': True}

    def create(self, validated_data):
        # Function needed to properly hash the password.
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RecipeSerializer(WritableNestedModelSerializer):
    """Recipe serializer."""
    ingredients = IngredientSerializer(many=True)
    steps = StepSerializer(many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
