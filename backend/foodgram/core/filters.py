from django_filters.rest_framework import filters, FilterSet

from recipe.models import Tag, Recipe
from users.models import User


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
    )

    is_favorited = filters.BooleanFilter(
        method='filters_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filters_shopping_cart',

    )

    class Meta:
        model = Recipe
        fields = [
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        ]

    def filters_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return Recipe.objects.all()

    def filters_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(basket__user=self.request.user)
        return Recipe.objects.all()
