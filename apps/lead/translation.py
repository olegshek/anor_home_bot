from modeltranslation import translator


from apps.lead.models import ResidentialProject, CommercialProject
from apps.lead.models.project import Location, Apartment, Store
from core.translation import TranslationOptionsMixin


@translator.register(Location)
class LocationOptions(TranslationOptionsMixin):
    fields = ('description',)


@translator.register(ResidentialProject)
class ResidentialProjectOptions(TranslationOptionsMixin):
    fields = ('description',)


@translator.register(CommercialProject)
class CommercialProjectOptions(TranslationOptionsMixin):
    fields = ('description',)


@translator.register(Apartment)
class ApartmentOptions(TranslationOptionsMixin):
    fields = ('description',)


@translator.register(Store)
class StoreOptions(TranslationOptionsMixin):
    fields = ('description',)
