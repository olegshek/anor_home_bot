from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.company.forms import ServiceForm, VacancyForm
from apps.company.models import CompanyText, CompanyPhoto, CompanyDocument, Service, Vacancy, ServiceRequest
from core.admin import TextAdmin


class ServiceAdmin(TranslationAdmin):
    form = ServiceForm


class VacancyAdmin(TranslationAdmin):
    form = VacancyForm


class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'customer', 'created_at')
    list_filter = ('customer', 'created_at')

    def has_change_permission(self, request, obj=None):
        return None

    def has_delete_permission(self, request, obj=None):
        return None

    def has_add_permission(self, request):
        return None


admin.site.register(CompanyText, TextAdmin)
admin.site.register(CompanyPhoto)
admin.site.register(CompanyDocument)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)
