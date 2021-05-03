from django.apps import AppConfig


class LeadConfig(AppConfig):
    name = 'apps.lead'

    def ready(self):
        from .signals import location_updated
