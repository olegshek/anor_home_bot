from django.contrib import admin

from apps.lead.models import ResidentialProject, CommercialProject, Apartment, Store
from apps.lead.models.project import Location

admin.site.register(ResidentialProject)
admin.site.register(CommercialProject)
admin.site.register(Location)
admin.site.register(Apartment)
admin.site.register(Store)