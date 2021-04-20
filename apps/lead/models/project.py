from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.file.models import Photo, Video, Document


class Location(models.Model):
    latitude = models.FloatField(verbose_name=_('Latitude'))
    longitude = models.FloatField(verbose_name=_('Longitude'))
    address = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=4000, verbose_name=_('Description'))


class Project(models.Model):
    name = models.CharField(max_length=48, verbose_name=_('Name'))
    description = models.CharField(max_length=150, verbose_name=_('Description'))

    class Meta:
        abstract = True


class ResidentialProject(Project):
    main_photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True,
                                   related_name='residential_projects_main', verbose_name=_('Main photo'))
    photos = models.ManyToManyField(Photo, related_name='residential_projects', blank=True, verbose_name=_('Photos'))
    videos = models.ManyToManyField(Video, related_name='residential_projects', blank=True, verbose_name=_('Videos'))
    documents = models.ManyToManyField(Document, related_name='residential_projects', blank=True,
                                       verbose_name=_('Documents'))
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, related_name='residential_project',
                                    verbose_name=_('Location'))

    catalog_documents = models.ManyToManyField(Document, related_name='document_residential_projects',
                                               verbose_name=_('Catalog documents'))


class CommercialProject(Project):
    main_photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True,
                                   related_name='commercial_projects_main', verbose_name=_('Main photo'))
    photos = models.ManyToManyField(Photo, related_name='commercial_projects', blank=True, verbose_name=_('Photos'))
    videos = models.ManyToManyField(Video, related_name='commercial_projects', blank=True, verbose_name=_('Videos'))
    documents = models.ManyToManyField(Document, related_name='commercial_projects', blank=True,
                                       verbose_name=_('Documents'))
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, related_name='commercial_project',
                                    verbose_name=_('Location'))

    catalog_documents = models.ManyToManyField(Document, related_name='document_commercial_projects',
                                               verbose_name=_('Catalog documents'))


class Apartment(models.Model):
    project = models.ForeignKey(ResidentialProject, on_delete=models.CASCADE, related_name='apartments',
                                verbose_name=_('Project'))
    room_quantity = models.PositiveIntegerField(verbose_name=_('Room quantity'))
    square = models.FloatField(verbose_name=_('Square'))
    description = models.CharField(max_length=198, verbose_name=_('Description'))

    photos = models.ManyToManyField(Photo, related_name='apartments', verbose_name=_('Photos'))


class Store(models.Model):
    project = models.ForeignKey(CommercialProject, on_delete=models.CASCADE, related_name='stores',
                                verbose_name=_('Project'))
    floor_number = models.PositiveIntegerField(verbose_name=_('Floor number'))
    square = models.FloatField(verbose_name=_('Square'))
    description = models.CharField(max_length=198, verbose_name=_('Description'))

    photos = models.ManyToManyField(Photo, related_name='stores', verbose_name=_('Photos'))
