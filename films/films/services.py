import os

import boto3
import requests_cache
import json

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
    for screenshot_data in screenshots_data:
        image = screenshot_data.pop('image')
        print(image.name, image.file, image.field_name, image.content_type, image.size, image.charset, sep='\n')
        Screenshot.objects.create(film=film, **screenshot_data)

        # implement connection with s3 and data transfer
        # aws_session = boto3.Session(
        #     aws_access_key_id=os.environ.get('ACCESS_KEY'),
        #     aws_secret_access_key=os.environ.get('SECRET_KEY'),
        # )
        # s3 = aws_session.client('s3')
        # response = s3.list_buckets()

        # Output the bucket names
        # print('Existing buckets:')
        # for bucket in response['Buckets']:
        #     print(f'  {bucket["Name"]}')

