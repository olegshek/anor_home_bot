# Generated by Django 3.1.7 on 2021-04-13 10:29

import core.utils
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommercialProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, verbose_name='Name')),
                ('description', models.CharField(max_length=150, verbose_name='Description')),
                ('documents', models.ManyToManyField(related_name='commercial_projects', to='file.Document', verbose_name='Documents')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(blank=True, max_length=20, null=True, verbose_name='Username')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Full name')),
                ('phone_number', models.CharField(max_length=20, null=True, verbose_name='Phone number')),
                ('language', models.CharField(choices=[('ru', 'Russian'), ('uz', 'Uzbek'), ('en', 'English')], max_length=2, null=True, verbose_name='Language')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('description', models.CharField(max_length=4000, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor_number', models.PositiveIntegerField(verbose_name='Floor number')),
                ('square', models.FloatField(verbose_name='Square')),
                ('description', models.CharField(max_length=198, verbose_name='Description')),
                ('photos', models.ManyToManyField(related_name='stores', to='file.Photo', verbose_name='Photos')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='lead.commercialproject', verbose_name='Project')),
            ],
        ),
        migrations.CreateModel(
            name='ResidentialProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, verbose_name='Name')),
                ('description', models.CharField(max_length=150, verbose_name='Description')),
                ('documents', models.ManyToManyField(related_name='residential_projects', to='file.Document', verbose_name='Documents')),
                ('location', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='residential_project', to='lead.location', verbose_name='Location')),
                ('main_photo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='residential_projects_main', to='file.photo', verbose_name='Main photo')),
                ('photos', models.ManyToManyField(related_name='residential_projects', to='file.Photo', verbose_name='Photos')),
                ('videos', models.ManyToManyField(related_name='residential_projects', to='file.Video', verbose_name='Videos')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=core.utils.generate_number)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='lead.customer', verbose_name='Customer')),
            ],
        ),
        migrations.AddField(
            model_name='commercialproject',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commercial_project', to='lead.location', verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='commercialproject',
            name='main_photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commercial_projects_main', to='file.photo', verbose_name='Main photo'),
        ),
        migrations.AddField(
            model_name='commercialproject',
            name='photos',
            field=models.ManyToManyField(related_name='commercial_projects', to='file.Photo', verbose_name='Photos'),
        ),
        migrations.AddField(
            model_name='commercialproject',
            name='videos',
            field=models.ManyToManyField(related_name='commercial_projects', to='file.Video', verbose_name='Videos'),
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_quantity', models.PositiveIntegerField(verbose_name='Room quantity')),
                ('square', models.FloatField(verbose_name='Square')),
                ('description', models.CharField(max_length=198, verbose_name='Description')),
                ('photos', models.ManyToManyField(related_name='apartments', to='file.Photo', verbose_name='Photos')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='lead.residentialproject', verbose_name='Project')),
            ],
        ),
    ]
