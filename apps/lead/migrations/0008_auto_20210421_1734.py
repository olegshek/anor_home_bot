# Generated by Django 3.1.7 on 2021-04-21 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0007_auto_20210420_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmenttransaction',
            name='lead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apartment_transactions', to='lead.lead', verbose_name='Lead'),
        ),
        migrations.AlterField(
            model_name='storetransaction',
            name='lead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_transactions', to='lead.lead', verbose_name='Lead'),
        ),
    ]
