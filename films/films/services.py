import os
import boto3
import requests_cache
import json
import pathlib
from PIL import Image

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
    # Path to temp screenshots dir
    file_dir = f'{settings.MEDIA_ROOT}/temp/{film.pk}/'

    # Path to temp compressed screenshots dir
    compressed_file_dir = f'{file_dir[:-1]}-compressed/'

    # Creating film (pk) screenshots folder
    _create_directory(file_dir)

    # Creating film (pk) compressed screenshots folder
    _create_directory(compressed_file_dir)

    for i, screenshot_data in enumerate(screenshots_data):
        image_data = screenshot_data.pop('image')
        image_format = image_data.content_type.split("/")[1]

        # Name of the file (e.g. 'screenshot-1.png')
        file_name = f'screenshot-{i+1}.{image_format}'

        file_path = f'{file_dir}{file_name}'
        compressed_file_path = f'{compressed_file_dir}{file_name}'

        with open(file_path, 'wb') as f:
            f.write(image_data.file.read())

        with open(compressed_file_path, 'wb') as f:
            f.write(image_data.file.read())

            # Image compressing code
            image = Image.open(file_path)
            resized_image = image.resize((314, 176))
            resized_image.save(f, format=image_format)

        Screenshot.objects.create(film=film, name=file_name)

    # s3 files uploading

    # Credentials
    aws_session = boto3.Session(
        aws_access_key_id=os.environ.get('ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('SECRET_KEY'),
    )
    s3 = aws_session.client('s3')
    for file, compressed_file in zip(pathlib.Path(file_dir).iterdir(),
                                     pathlib.Path(compressed_file_dir).iterdir()):
        s3.upload_file(file.absolute(), 'films-screenshots', f'{film.pk}/{file.name}')
        s3.upload_file(compressed_file.absolute(), 'films-compressed-screenshots', f'{film.pk}/{compressed_file.name}')

    _clear_directory(file_dir)
    _clear_directory(compressed_file_dir)


def _create_directory(path: str):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def _clear_directory(path: str):
    for file in pathlib.Path(path).iterdir():
        try:
            os.remove(file.absolute())
        except FileNotFoundError:
            pass

    try:
        os.rmdir(path)
    except FileNotFoundError:
        pass



