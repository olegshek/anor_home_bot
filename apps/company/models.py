from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.file.models import Photo, Document
from apps.lead.models import Customer
from core.utils import generate_number


class CompanyText(models.Model):
    text = models.CharField(max_length=4000, verbose_name=_('Text'))

    class Meta:
        verbose_name = _('Company text')
        verbose_name_plural = _('Company text')

    def __str__(self):
        return self.text_ru


class CompanyPhoto(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, related_name='company_photo', verbose_name=_('Photo'))

    class Meta:
        verbose_name = _('Company photo')
        verbose_name_plural = _('company photos')

    def __str__(self):
        return self.photo.photo.name


class CompanyDocument(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='company_document',
                                    verbose_name=_('Document'))

    class Meta:
        verbose_name = _('Company document')
        verbose_name_plural = _('Company documents')

    def __str__(self):
        return self.document.document.name


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.CharField(max_length=200, verbose_name=_('Description'))
    photo = models.OneToOneField(Photo, on_delete=models.RESTRICT, related_name='service', verbose_name=_('Photo'))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return self.name_ru


class Vacancy(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.CharField(max_length=200, verbose_name=_('Description'))
    photo = models.OneToOneField(Photo, on_delete=models.RESTRICT, related_name='vacancy', verbose_name=_('Photo'))

    class Meta:
        verbose_name = _('Vacancy')
        verbose_name_plural = _('Vacancies')

    def __str__(self):
        return self.name_ru


class ServiceRequest(models.Model):
    number = models.IntegerField(default=generate_number, verbose_name=_('Number'))
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests', verbose_name=_('Service'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_requests',
                                 verbose_name=_('Customer'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created at'))


class VacancyRequest(models.Model):
    number = models.IntegerField(default=generate_number, verbose_name=_('Number'))
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='requests', verbose_name=_('Vacancy'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vacancy_requests',
                                 verbose_name=_('Customer'))
    cv_file_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created at'))
