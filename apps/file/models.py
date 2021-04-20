from django.db import models
from django.utils.translation import gettext_lazy as _


class File(models.Model):
    description = models.CharField(max_length=198, null=True, blank=True, verbose_name=_('Description'))

    class Meta:
        abstract = True


class Photo(File):
    photo = models.ImageField(verbose_name=_('Photo'))

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __str__(self):
        return self.photo.name


class Document(File):
    document = models.FileField(verbose_name=_('Document'))

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def __str__(self):
        return self.document.name


class Video(File):
    video = models.FileField(verbose_name=_('Video'))

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __str__(self):
        return self.video.name
