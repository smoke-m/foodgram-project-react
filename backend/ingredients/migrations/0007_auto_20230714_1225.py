# Generated by Django 3.2.16 on 2023-07-14 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0006_alter_ingredient_name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ingredient',
            name='unique_ingredient',
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='уникальность_ингредиента_измерение.'),
        ),
    ]
