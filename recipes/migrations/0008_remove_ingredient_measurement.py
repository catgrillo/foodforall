# Generated by Django 3.1.1 on 2020-11-26 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_ingredient_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='measurement',
        ),
    ]