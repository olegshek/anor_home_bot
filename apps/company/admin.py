from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.company.forms import ServiceForm, VacancyForm
from apps.company.models import CompanyText, CompanyPhoto, CompanyDocument, Service, Vacancy
from core.admin import TextAdmin


class ServiceAdmin(TranslationAdmin):
    form = ServiceForm


class VacancyAdmin(TranslationAdmin):
    form = VacancyForm


admin.site.register(CompanyText, TextAdmin)
admin.site.register(CompanyPhoto)
admin.site.register(CompanyDocument)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Vacancy, VacancyAdmin)
