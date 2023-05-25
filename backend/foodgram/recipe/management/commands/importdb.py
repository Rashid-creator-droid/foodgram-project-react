import json

from django.core.management.base import BaseCommand

from recipe.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/ingredients.json', 'rb') as f:
            data = json.load(f)
            ingredients = Ingredient()
            index = 1
            for ingredient in data:
                ingredients.pk = index
                ingredients.name = ingredient.get('name')
                ingredients.measurement_unit = ingredient.get(
                    'measurement_unit'
                )
                ingredients.save()
                index += 1
        print('finished')
