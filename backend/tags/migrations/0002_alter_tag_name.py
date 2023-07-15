# Generated by Django 3.2.16 on 2023-07-15 08:32

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Введите название тага', max_length=64, unique=True, validators=[api.validators.validate_name], verbose_name='Название тага'),
        ),
    ]
