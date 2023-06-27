from django.core.validators import MinValueValidator


def min_validator():
    return [
        MinValueValidator(1, 'Хоть 1 поставь!')
    ]
