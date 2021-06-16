# Generated by Django 3.1.7 on 2021-06-16 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0003_delete_video'),
        ('lead', '0015_auto_20210612_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='photos',
        ),
        migrations.AddField(
            model_name='apartment',
            name='photos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apartments', to='file.photo', verbose_name='Photo'),
        ),
        migrations.RemoveField(
            model_name='store',
            name='photos',
        ),
        migrations.AddField(
            model_name='store',
            name='photos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='file.photo', verbose_name='Photo'),
        ),
    ]
