# Generated by Django 3.1.1 on 2020-11-26 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_remove_ingredient_measurement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]