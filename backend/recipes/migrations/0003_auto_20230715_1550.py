# Generated by Django 3.2.16 on 2023-07-15 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0002_alter_ingredient_options'),
        ('recipes', '0002_auto_20230715_1533'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепты', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='ingredient',
            field=models.ForeignKey(help_text='Выберите из списка', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='ingredients.ingredient', verbose_name='Ингредиент'),
        ),
    ]