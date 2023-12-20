from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


MAX_NAME_LENGTH = 200


class Ingredient(models.Model):
    """Модель данных для ингредиентов ."""
    name = models.CharField(
        'Название',
        max_length=MAX_NAME_LENGTH,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.name}'


class Recipe(models.Model):
    """Модель данных для рецептов."""
    name = models.CharField(
        'Название',
        max_length=MAX_NAME_LENGTH,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return f'{self.name}'


class RecipeIngredient(models.Model):
    """Связующая модель для рецептов и ингредиентов."""
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipeingredient',
        on_delete=models.PROTECT)
    amount = models.IntegerField(
        'Количество')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
