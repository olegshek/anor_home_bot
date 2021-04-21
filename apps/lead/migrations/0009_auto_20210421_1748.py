# Generated by Django 3.1.7 on 2021-04-21 12:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0008_auto_20210421_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='apartmenttransaction',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='storetransaction',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False),
        ),
    ]
