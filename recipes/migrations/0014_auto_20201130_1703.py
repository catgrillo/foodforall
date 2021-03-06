# Generated by Django 3.1.1 on 2020-11-30 17:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0013_auto_20201130_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(validators=[django.core.validators.MinLengthValidator(1, 'Ingredient must be greater than 1 character')])),
                ('measurement', models.TextField(validators=[django.core.validators.MinLengthValidator(1, 'Ingredient measurement must be greater than 1 character')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipe_ingredient', through='recipes.Ingredient', to=settings.AUTH_USER_MODEL),
        ),
    ]
