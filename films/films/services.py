import os
import boto3
import requests_cache
import json
import pathlib

from django.conf import settings
from .models import Screenshot


def get_cached_imdb_response(validated_data) -> str:
    session = requests_cache.CachedSession(cache_name=f'{os.path.dirname(__file__)}/cache/imdb-cache', backend='sqlite',
                                           expire_after=600)
    # fix error: raise ConnectionError(e, request=request)
    # cinema-films-1  | requests.exceptions.ConnectionError: HTTPSConnectionPool(host='imdb-api.com', port=443):
    # Max retries exceeded with url: /en/API/Ratings/k_92xc2azh/tt1375666
    # (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f62410b6290>:
    # Failed to establish a new connection: [Errno -3] Try again'))
    response = json.loads((session.get(
        'https://imdb-api.com/en/API/Ratings/k_92xc2azh/%s' % validated_data.pop('imdb_id')).content.decode('utf-8')))
    return response['imDb']


def initialize_screenshots(screenshots_data, film):
    for i, screenshot_data in enumerate(screenshots_data):
        image_data = screenshot_data.pop('image')
        image_format = image_data.content_type.split("/")[1]
        file_path = os.path.join(settings.MEDIA_ROOT, f'temp/{film.pk}/screenshot-{i+1}.{image_format}')
        try:
            os.mkdir(os.path.join(settings.MEDIA_ROOT, f'temp/{film.pk}'))
        except FileExistsError:
            pass
        with open(file_path, 'wb') as f:
            f.write(image_data.file.read())
        Screenshot.objects.create(film=film, name=f'screenshot-{i+1}.{image_format}')

    # s3 files uploading
    # aws_session = boto3.Session(
    #     aws_access_key_id=os.environ.get('ACCESS_KEY'),
    #     aws_secret_access_key=os.environ.get('SECRET_KEY'),
    # )
    # s3 = aws_session.client('s3')
    # for file in pathlib.Path(f'{settings.MEDIA_ROOT}/temp/{film.pk}').iterdir():
    #     s3.upload_file(file.absolute(), 'films-screenshots', f'{film.pk}/{file.name}')

    for file in pathlib.Path(f'{settings.MEDIA_ROOT}/temp/{film.pk}').iterdir():
        try:
            os.remove(file.absolute())
        except FileNotFoundError:
            pass

    try:
        os.rmdir(f'{settings.MEDIA_ROOT}/temp/{film.pk}')
    except FileNotFoundError:
        pass



