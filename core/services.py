import json
import time

import requests
from django.conf import settings

from core.exceptions import GMapsServiceError


def get_geocode(data):
    params = {
        'address': f'{data[1]}+{data[0]},+Tashkent,+UZ' if type == 'address' else f'{data[0]}, {data[1]}',
        'key': settings.GOOGLE_MAPS_TOKEN
    }

    for i in range(5):
        try:
            response = requests.get(url=settings.GOOGLE_MATRIX_URL+'/geocode/json?', params=params)
        except IOError:
            raise GMapsServiceError('No connection')

        data = json.loads(response.content)

        if data['status'] == 'OK':
            for result in data['results']:
                geometry = result.get('geometry', None)
                address = result.get('formatted_address', None)
                if geometry and geometry.get('location', None) and address:
                    return {'latlng': geometry['location'], 'address': address}

        elif data['status'] != 'UNKNOWN_ERROR':
            raise GMapsServiceError(data['status'])
        else:
            time.sleep(1.5)

    raise GMapsServiceError('No response')

