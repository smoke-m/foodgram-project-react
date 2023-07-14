import csv

from django.core.management.base import BaseCommand

from foodgram.settings import CSV_FILES_DIR
from ingredients.models import Ingredient


class Command(BaseCommand):
    """Команда загрузки ингредиентов в базу."""
    help = 'Загрузка ингредиентов в базу.'

    def handle(self, *args, **kwargs):
        with open(
                f'{CSV_FILES_DIR}/ingredients.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            next(reader)
            ingredients = [
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1],
                )
                for row in reader
            ]
            Ingredient.objects.bulk_create(ingredients)
        print('Ингредиенты загружены')
        print('Добавленно:', Ingredient.objects.count(), 'Ингредиентов')
