# Generated by Django 4.1.7 on 2023-03-21 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('poster_name', models.CharField(max_length=100)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=4)),
                ('country', models.CharField(max_length=50)),
                ('realese_date', models.DateField()),
                ('director', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('age_restriction', models.IntegerField()),
                ('studio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='films.film')),
            ],
        ),
    ]
