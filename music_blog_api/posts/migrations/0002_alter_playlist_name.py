# Generated by Django 3.2.16 on 2023-11-14 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название плейлиста'),
        ),
    ]
