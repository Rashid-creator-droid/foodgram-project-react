from rest_framework.validators import ValidationError

from recipe.models import Ingredient


def validate_ingredients(data):
    if not data:
        raise ValidationError(
            {'ingredients': 'Обязательное поле.'}
        )
    if len(data) < 1:
        raise ValidationError(
            {'ingredients': 'Отсутствуют ингредиенты'}
        )
    unique_ingredient = []
    for ingredient in data:
        if not Ingredient.objects.filter(
                id=ingredient.get('id')
        ).exists():
            raise ValidationError(
                {'ingredients': 'Такого ингредиента нет'}
            )
        if id in unique_ingredient:
            raise ValidationError(
                {'ingredients': 'Повторы запрещены'}
            )
        unique_ingredient.append(id)
        amount = int(ingredient.get('amount'))
        if amount < 1:
            raise ValidationError(
                {'amount': 'Количество не может быть меньше 1'}
            )
        if amount > 1000:
            raise ValidationError(
                {'amount': 'Количество не может быть меньше 1000'}
            )
    return data
