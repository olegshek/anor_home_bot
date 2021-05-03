# Generated by Django 3.1.7 on 2021-05-03 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0013_auto_20210503_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.FloatField(null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.FloatField(null=True, verbose_name='Longitude'),
        ),
    ]
