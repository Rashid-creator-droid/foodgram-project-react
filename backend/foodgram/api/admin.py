from django.contrib import admin
from users.models import User

from recipe.models import Ingredients, Recipe, Tag


class UnitAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )

class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientsInLine,
    ]

admin.site.register(Tag)
admin.site.register(Ingredients)
admin.site.register(User)
# admin.site.register(Unit, UnitAdmin)
