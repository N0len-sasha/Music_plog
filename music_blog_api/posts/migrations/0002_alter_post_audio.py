# Generated by Django 3.2.16 on 2023-11-08 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='posts/audio/'),
        ),
    ]
