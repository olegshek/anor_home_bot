# Generated by Django 3.1.7 on 2021-05-22 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20210503_1600'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicerequest',
            options={'ordering': ('-created_at',), 'verbose_name': 'Service request', 'verbose_name_plural': 'Service requests'},
        ),
    ]