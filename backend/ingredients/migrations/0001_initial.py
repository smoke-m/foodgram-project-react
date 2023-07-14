# Generated by Django 3.2.16 on 2023-07-14 12:51

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите имя ингредиента', max_length=64, unique=True, validators=[api.validators.validate_name], verbose_name='Имя ингредиента')),
                ('measurement_unit', models.CharField(help_text='Укажите единицы измерения', max_length=10, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='уникальность_ингредиента_измерение.'),
        ),
    ]
