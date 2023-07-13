from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator


def min_validator():
    return [
        MinValueValidator(1, 'Хоть 1 поставь!')
    ]


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Имя не может быть "me"')


def validate_name(value):
    regex = r'^[A-Za-z0-9А-Яа-я\s()]+$'
    error_message = 'Разрешены только буквы, цифры и пробел.'
    validator = RegexValidator(regex=regex, message=error_message)
    validator(value)
