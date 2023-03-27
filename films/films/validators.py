import requests
import requests_cache
import os
import json

from rest_framework.serializers import ValidationError


def validate_imdb_id(value):
    if value[:2] != 'tt':
        raise ValidationError('Imdb film id must start with "tt"')
    
    session = requests_cache.CachedSession(cache_name=f'{os.path.dirname(__file__)}/cache/imdb-cache', backend='sqlite', expire_after=600)
    response = json.loads((session.get('https://imdb-api.com/en/API/Ratings/k_92xc2azh/%s' % value).content.decode('utf-8')))
    if response['errorMessage']:
        raise ValidationError('Invalid ImDb film id')
    return value
    

def validate_rating(value):
    if value < 0.00 or value > 10.00:
        raise ValidationError('Rating must be from 0.00 to 10.00')
    return value


def validate_age_restriction(value):
    if not 0 <= value <= 21:
        raise ValidationError('Age restriction must be from 0 to 21')
    return value
