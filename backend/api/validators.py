from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


def min_validator():
    return [
        MinValueValidator(1, 'Хоть 1 поставь!')
    ]


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Имя не может быть "me"')
