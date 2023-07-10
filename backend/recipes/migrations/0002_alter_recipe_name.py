# Generated by Django 3.2.16 on 2023-07-09 13:52

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Ведите название рецепта', max_length=32, validators=[api.validators.validate_name], verbose_name='Название рецепта'),
        ),
    ]