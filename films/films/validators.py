import requests_cache
import os
import json

from rest_framework.serializers import ValidationError
from django.core.validators import RegexValidator


def validate_imdb_id(value):
    if value[:2] != 'tt':
        raise ValidationError('Imdb film id must start with "tt"')
    
    session = requests_cache.CachedSession(cache_name=f'{os.path.dirname(__file__)}/cache/imdb-cache', backend='sqlite', expire_after=600)
    try:
        response = json.loads((session.get('https://imdb-api.com/en/API/Ratings/k_92xc2azh/%s' % value).content.decode('utf-8')))
        if response['errorMessage']:
            raise ValidationError('Invalid ImDb film id')
    except ConnectionError as e:
        raise ValidationError(e.message)
    return value
    

def validate_rating(value):
    if not 0.00 <= value <= 10.00:
        raise ValidationError('Rating must be from 0.00 to 10.00')
    return value


def validate_age_restriction(value):
    if not 0 <= value <= 21:
        raise ValidationError('Age restriction must be from 0 to 21')
    return value


def validate_text(value):
    language_validator = RegexValidator(
        regex=r'^[A-Za-z0-9А-Яа-яЇїІіЄєҐґ:?!\-\+\(\)\.,ʼ=№#& ]+$',
        message='Text format is not allowed',
    )
    
    try:
        language_validator(value)
    except ValidationError as e:
        raise ValidationError(e.message, code='invalid_text')


def validate_image(value):
    # Image size validation

    size_mb = value.file.getbuffer().nbytes / (1024 * 1024)
    if size_mb > 10:
        raise ValidationError(f"File size must be under 10 MB")
    return value
