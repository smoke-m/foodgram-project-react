# Generated by Django 3.2.16 on 2023-07-05 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0003_auto_20230702_1818'),
        ('recipes', '0007_alter_recipeingredients_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredients',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.ingredient', verbose_name='Ингредиент'),
        ),
    ]
