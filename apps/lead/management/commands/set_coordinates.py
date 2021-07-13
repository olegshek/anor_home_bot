from django.core.management import BaseCommand

from apps.lead.models.project import Location
from apps.lead.tasks import set_location_coordinates


class Command(BaseCommand):
    def handle(self, *args, **options):
        for location in Location.objects.all():
            set_location_coordinates.delay(location.id)