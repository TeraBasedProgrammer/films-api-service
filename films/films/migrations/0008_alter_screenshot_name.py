# Generated by Django 4.1.7 on 2023-03-31 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0007_alter_screenshot_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screenshot',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
