from rest_framework.validators import ValidationError

from foodgram.settings import MIN_AMOUNT, MAX_AMOUNT


def validate_ingredients(data):
    if not data:
        raise ValidationError(
            {'ingredients': 'Обязательное поле.'}
        )
    for ingredient in data:
        amount = int(ingredient.get('amount'))
        if amount < MIN_AMOUNT:
            raise ValidationError(
                {'amount': 'Количество не может быть меньше 1'}
            )
        if amount > MAX_AMOUNT:
            raise ValidationError(
                {'amount': 'Количество не может быть меньше 1000'}
            )
    return data
