from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.file.models import Photo, Document


class CompanyText(models.Model):
    text = models.CharField(max_length=4000, verbose_name=_('Text'))


class CompanyPhoto(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, related_name='company_photo', verbose_name=_('Photo'))


class CompanyDocument(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='company_document',
                                    verbose_name=_('Document'))


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.CharField(max_length=200, verbose_name=_('Description'))
    photo = models.OneToOneField(Photo, on_delete=models.RESTRICT, related_name='service', verbose_name=_('Photo'))


class Vacancy(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.CharField(max_length=200, verbose_name=_('Description'))
    photo = models.OneToOneField(Photo, on_delete=models.RESTRICT, related_name='vacancy', verbose_name=_('Photo'))
