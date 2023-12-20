from django.db.models import Prefetch
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from api.serializers import (IngredientSerializer, RecipeCreateSerializer,
                             RecipeSerializer)
from recipes.models import Ingredient, Recipe, RecipeIngredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для объектов модели ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


@method_decorator(cache_page(60 * 15), name='list')
class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания/редактирования и просмотра рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    http_method_names = ('get', 'post', 'patch', 'delete', )

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer

        return RecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all().select_related(
            'author').prefetch_related(
                Prefetch('recipe_ingredients',
                         queryset=RecipeIngredient.objects.select_related(
                             'ingredient')))
        return queryset
