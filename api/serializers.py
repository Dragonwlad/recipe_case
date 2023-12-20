from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from recipes.models import (Ingredient, Recipe,
                            RecipeIngredient)


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор ингредиентов.'''
    class Meta:
        model = Ingredient
        fields = ('id', 'name', )


class IngredientShowSerializer(serializers.ModelSerializer):
    '''Сериализатор отображения ингредиентов с количеством в рецептах.'''
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = RecipeIngredient
        fields = ('id',
                  'name',
                  'amount'
                  )


class RecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор отображения рецептов.'''
    ingredients = IngredientShowSerializer(
        many=True, source='recipe_ingredients', read_only=True,)
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ('id',
                  'author',
                  'ingredients',
                  'name',
                  'text',
                  )


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор сохранения ингредиентов в рецептах.'''
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', )


class RecipeCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор создания рецептов.'''
    ingredients = RecipeIngredientCreateSerializer(many=True, required=True)

    class Meta:
        model = Recipe
        fields = ('ingredients',
                  'name',
                  'text',
                  )

    def to_representation(self, instance):
        '''Функция для передачи request в context, для получения данных
        о пользователе в сериализаторах.'''
        serializer = RecipeSerializer(
            instance,
            context={'request': self.context.get('request')})
        return serializer.data

    def create_update_recipe(self, ingredients_data, recipe):
        '''Функция для сохранения/обновления вложенных полей рецепта.'''
        recipe_ingredients = []
        for ingredient_data in ingredients_data:
            recipe_ingredients.append(RecipeIngredient(recipe=recipe,
                                                       **ingredient_data))
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    @transaction.atomic
    def create(self, validated_data):
        '''Функция для сохранения вложенных полей.'''
        user = self.context['request'].user
        validated_data['author'] = user
        ingredients_data = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        self.create_update_recipe(ingredients_data, recipe)
        return recipe

    @transaction.atomic
    def update(self, validated_data, instance):
        '''Функция для обновления вложенных полей.'''
        ingredients_data = instance.pop('ingredients')
        validated_data.ingredients.clear()
        self.create_update_recipe(ingredients_data, validated_data)
        return super().update(validated_data, instance)
