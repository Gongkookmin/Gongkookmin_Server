# Generated by Django 2.2.7 on 2019-12-02 07:09

import api_server.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_server', '0005_auto_20191201_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='expires',
            field=models.CharField(default='none', max_length=10),
        ),
        migrations.AddField(
            model_name='offer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=api_server.models.get_file_path),
        ),
        migrations.AddField(
            model_name='offer',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=api_server.models.get_file_path),
        ),
        migrations.AddField(
            model_name='offer',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=api_server.models.get_file_path),
        ),
    ]
