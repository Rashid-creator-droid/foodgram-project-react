from rest_framework.validators import ValidationError


def validate_ingredients(data):
    if not data:
        raise ValidationError(
            {'ingredients': 'Обязательное поле.'}
        )
    if len(data) < 1:
        raise ValidationError(
            {'ingredients': 'Отсутствуют ингредиенты'}
        )
    for ingredient in data:
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
