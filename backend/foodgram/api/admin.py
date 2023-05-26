from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.safestring import mark_safe

from recipe.models import Ingredient, Recipe, Tag, Favorites, Basket
from users.models import User, Follow


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


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    form = UserChangeForm
    model = User
    search_fields = (
        'username',
        'email',
    )
    list_filter = (
        'username',
        'email',
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

    @staticmethod
    def preview(obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 50px;">'
        )

    @staticmethod
    def favorite_count(obj):
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
