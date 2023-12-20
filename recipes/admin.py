from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredient

admin.site.empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    list_filter = ('name', )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline, ]
    list_display = ('name', 'author', )
    search_fields = ('name',)
    list_filter = ('author', 'name', )
    fields = ('author',
              'name',
              'text',
              )
