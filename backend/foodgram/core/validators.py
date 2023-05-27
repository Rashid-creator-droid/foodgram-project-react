from rest_framework.validators import ValidationError
from django.core.exceptions import ValidationError as ValidateModelImage
from django.conf import settings


def file_size(value):
    limit = settings.IMAGE_SIZE
    if value.size > limit:
        raise ValidateModelImage(
            'Размер изображения не должен превышать 512 kb.'
        )


def validate_ingredients(data):
    if not data:
        raise ValidationError(
            {'ingredients': 'Обязательное поле.'}
        )
    for ingredient in data:
        amount = int(ingredient.get('amount'))
        if amount < settings.MIN_AMOUNT:
            raise ValidationError(
                {'amount': 'Количество не может быть меньше 1'}
            )
        if amount > settings.MAX_AMOUNT:
            raise ValidationError(
                {'amount': 'Количество не может быть меньше 1000'}
            )
    return data
