# Generated by Django 4.1.7 on 2023-06-30 19:38

from django.db import migrations, models
import films.validators


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0006_alter_actor_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=50, unique=True, validators=[films.validators.validate_names]), unique=True),
        ),
    ]