from django.contrib import admin
from django.utils.safestring import mark_safe

from recipe.models import Ingredient, Recipe, Tag, Favorites, Basket
from users.models import Follow


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'measurement_unit',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'preview',
        'favorite_count',
    )
    search_fields = (
        'name',
        'author__username',
        'tags__name',
    )
    list_filter = (
        'name',
        'author__username',
        'tags__name',
    )

    inlines = (
        IngredientsInLine,
    )

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 50px;">'
        )

    def favorite_count(self, obj):
        return obj.favorite.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
    )


@admin.register(Favorites)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = (
        'user__username',
        'recipe__name',
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )
    search_fields = (
        'user__username',
        'author__username',
    )


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = (
        'user__username',
        'recipe__name',
    )
