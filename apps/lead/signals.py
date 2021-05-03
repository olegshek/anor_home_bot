from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.lead.models.project import Location
from apps.lead.tasks import set_location_coordinates


@receiver(post_save, sender=Location)
def location_updated(sender, instance, *args, **kwargs):
    if kwargs['created']:
        set_location_coordinates.delay(instance.id)
