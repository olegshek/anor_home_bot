from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.lead.forms import ProjectForm, LocationForm, ApartmentForm, StoreForm
from apps.lead.models import ResidentialProject, CommercialProject, Apartment, Store, ApartmentTransaction, \
    StoreTransaction, Lead
from apps.lead.models.lead import DuplexTransaction
from apps.lead.models.project import Location, Duplex


class ProjectAdmin(TranslationAdmin):
    form = ProjectForm
    filter_horizontal = ('photos', 'documents', 'catalogue_documents')


class LocationAdmin(TranslationAdmin):
    form = LocationForm


class ApartmentAdmin(admin.ModelAdmin):
    form = ApartmentForm
    list_display = ('__str__', 'project', 'room_quantity', 'square', 'duplex', 'floor_number')
    filter_horizontal = ('photos', )
    list_filter = ('project', 'duplex', 'room_quantity')


class StoreAdmin(TranslationAdmin):
    form = StoreForm
    list_display = ('__str__', 'project', 'square', 'floor_number')
    filter_horizontal = ('photos',)
    list_filter = ('project',)


class CustomerAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return None

    def has_delete_permission(self, request, obj=None):
        return None

    def has_add_permission(self, request):
        return None


class DuplexAdmin(admin.ModelAdmin):
    list_filter = ('project',)


class ApartmentTransactionAdminInline(admin.StackedInline):
    model = ApartmentTransaction
    fk_name = 'lead'


class StoreTransactionAdminInline(admin.StackedInline):
    model = StoreTransaction
    fk_name = 'lead'


class DuplexTransactionAdminInline(admin.StackedInline):
    model = DuplexTransaction
    fk_name = 'lead'


class LeadAdmin(admin.ModelAdmin):
    inlines = [ApartmentTransactionAdminInline, StoreTransactionAdminInline, DuplexTransactionAdminInline]
    list_display = ('__str__', 'customer', 'created_at')
    list_filter = ('customer', 'created_at')

    def has_change_permission(self, request, obj=None):
        return None

    def has_delete_permission(self, request, obj=None):
        return None

    def has_add_permission(self, request):
        return None


admin.site.register(ResidentialProject, ProjectAdmin)
admin.site.register(CommercialProject, ProjectAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Duplex, DuplexAdmin)
admin.site.register(Lead, LeadAdmin)
