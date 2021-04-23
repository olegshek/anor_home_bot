from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.file.models import Photo
from apps.lead.models.project import Location


class ContactLocation(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE, related_name='contact_location',
                                    verbose_name=_('Location'))


class ContactText(models.Model):
    text = models.CharField(max_length=4000, verbose_name=_('Text'))


class ContactPhoto(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, related_name='contact_photo', verbose_name=_('Photo'))
