import logging
import sys

from apps.lead.models.project import Location
from config.celery import app
from core.exceptions import GMapsServiceError
from core.services import get_geocode


@app.task
def set_location_coordinates(location_id):
    location = Location.objects.get(id=location_id)

    try:
        geocode_data = get_geocode(location.address)
    except GMapsServiceError:
        logger = logging.getLogger('django')
        return logger.error(
            'Internal Server Error: Google Maps Matrix Service Error',
            exc_info=sys.exc_info(),
            extra={'status_code': 500, 'request': None},
        )

    location.latitude = geocode_data['latlng']['lat']
    location.longitude = geocode_data['latlng']['lng']
    location.save()
