from modeltranslation import translator

from apps.company.models import CompanyText, Service, Vacancy
from core.translation import TranslationOptionsMixin


@translator.register(CompanyText)
class CompanyTextOptions(TranslationOptionsMixin):
    fields = ('text',)


@translator.register(Service)
class ServiceOptions(TranslationOptionsMixin):
    fields = ('name', 'description')


@translator.register(Vacancy)
class VacancyOptions(TranslationOptionsMixin):
    fields = ('name', 'description')
