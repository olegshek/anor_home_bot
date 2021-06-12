from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.file.models import Photo, Document


class Location(models.Model):
    latitude = models.FloatField(null=True, blank=True, verbose_name=_('Latitude'))
    longitude = models.FloatField(null=True, blank=True, verbose_name=_('Longitude'))
    address = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=4000, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return self.address


class Project(models.Model):
    name = models.CharField(max_length=48, verbose_name=_('Name'))
    description = models.CharField(max_length=150, verbose_name=_('Description'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ResidentialProject(Project):
    main_photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True,
                                   related_name='residential_projects_main', verbose_name=_('Main photo'))
    photos = models.ManyToManyField(Photo, related_name='residential_projects', blank=True, verbose_name=_('Photos'))
    documents = models.ManyToManyField(Document, related_name='residential_projects', blank=True,
                                       verbose_name=_('Documents'))
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, related_name='residential_project',
                                    verbose_name=_('Location'))

    catalogue_documents = models.ManyToManyField(Document, related_name='catalogue_residential_projects',
                                                 verbose_name=_('Catalog documents'))

    class Meta:
        verbose_name = _('Residential project')
        verbose_name_plural = _('Residential projects')

    def __str__(self):
        return self.name


class CommercialProject(Project):
    main_photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True,
                                   related_name='commercial_projects_main', verbose_name=_('Main photo'))
    photos = models.ManyToManyField(Photo, related_name='commercial_projects', blank=True, verbose_name=_('Photos'))
    documents = models.ManyToManyField(Document, related_name='commercial_projects', blank=True,
                                       verbose_name=_('Documents'))
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, related_name='commercial_project',
                                    verbose_name=_('Location'))

    catalogue_documents = models.ManyToManyField(Document, related_name='catalogue_commercial_projects',
                                                 verbose_name=_('Catalog documents'))

    class Meta:
        verbose_name = _('Commercial project')
        verbose_name_plural = _('Commercial projects')

    def __str__(self):
        return self.name


class Duplex(models.Model):
    project = models.ForeignKey(ResidentialProject, on_delete=models.CASCADE, related_name='duplexes',
                                verbose_name=_('Project'))
    room_quantity = models.IntegerField()

    class Meta:
        verbose_name = _('Duplex')
        verbose_name_plural = _('Duplexes')

    def __str__(self):
        return f'{self.project.name}-{self.room_quantity}'


class Apartment(models.Model):
    project = models.ForeignKey(ResidentialProject, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='apartments', verbose_name=_('Project'))
    duplex = models.ForeignKey(Duplex, on_delete=models.SET_NULL, null=True, blank=True, related_name='apartments',
                               verbose_name=_('Duplex'))
    room_quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Room quantity'))
    square = models.FloatField(verbose_name=_('Square'))
    description = models.CharField(max_length=198, verbose_name=_('Description'))
    floor_number = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Floor number'))

    photos = models.ManyToManyField(Photo, related_name='apartments', verbose_name=_('Photos'))

    class Meta:
        verbose_name = _('Apartment')
        verbose_name_plural = _('Apartments')

    def __str__(self):
        return f'{self.project.name if self.project else self.duplex.project.name}-{self.room_quantity}-{self.square}'


class Store(models.Model):
    project = models.ForeignKey(CommercialProject, on_delete=models.CASCADE, related_name='stores',
                                verbose_name=_('Project'))
    floor_number = models.PositiveIntegerField(verbose_name=_('Floor number'))
    square = models.FloatField(verbose_name=_('Square'))
    description = models.CharField(max_length=198, verbose_name=_('Description'))

    photos = models.ManyToManyField(Photo, related_name='stores', verbose_name=_('Photos'))

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return f'{self.project.name}-{self.floor_number}-{self.square}'