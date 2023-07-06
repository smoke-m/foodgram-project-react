import re

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


def min_validator():
    return [
        MinValueValidator(1, 'Хоть 1 поставь!')
    ]


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Имя не может быть "me"')


def validate_name(value):
    pattern = r'^[A-Za-z0-9\s]+$'
    if not re.match(pattern, value):
        raise ValidationError('Разрешено только буквы и цифры.')
