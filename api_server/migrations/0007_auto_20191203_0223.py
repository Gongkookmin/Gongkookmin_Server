# Generated by Django 2.2.7 on 2019-12-02 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_server', '0006_auto_20191202_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='body',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='offer',
            name='title',
            field=models.CharField(max_length=20),
        ),
    ]