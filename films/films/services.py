import os
import requests_cache
import json
import pathlib
import logging

from PIL import Image
from django.conf import settings
from django.db.models import Model
from django.core.exceptions import ValidationError
from .models import Screenshot, Film
from actors.models import Actor


logger = logging.getLogger('logger')


def get_cached_imdb_response(imdb_id) -> str:
    """
    Retrieves film imdb rating (directly or from cache)
    @param imdb_id: imdb id for IMDB API (e.g. tt1375666)
    @return: imdb rating string (e.g. '8.80')
    """
    try:
        session = requests_cache.CachedSession(cache_name=f'{os.path.dirname(__file__)}/cache/imdb-cache', backend='sqlite',
                                           expire_after=600)
        # fix error: raise ConnectionError(e, request=request)
        # cinema-films-1  | requests.exceptions.ConnectionError: HTTPSConnectionPool(host='imdb-api.com', port=443):
        # Max retries exceeded with url: /en/API/Ratings/k_92xc2azh/tt1375666
        # (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f62410b6290>:
        # Failed to establish a new connection: [Errno -3] Try again'))
        response = json.loads((session.get(
            'https://imdb-api.com/en/API/Ratings/k_92xc2azh/%s' % imdb_id).content.decode('utf-8')))
        return response['imDb']
    except ConnectionError:
        raise ValidationError('Connection error, try again')


def initialize_images(poster_image, screenshots_data, film):
    # Path to temp screenshots dir
    file_dir = f'{settings.MEDIA_ROOT}/temp/{film.pk}/'

    # Path to temp compressed screenshots dir
    compressed_file_dir = f'{file_dir[:-1]}-compressed/'

    # Creating film (pk) screenshots folder
    create_directory(file_dir)

    # Creating film (pk) compressed screenshots folder
    create_directory(compressed_file_dir)

    poster_file = f'{file_dir}poster.{film.poster_format}'

    # Poster file creation
    with open(poster_file, 'wb') as f:
        f.write(poster_image.file.read())

    # Screenshots files creation
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

            # Image compressing
            image = Image.open(file_path)
            resized_image = image.resize((314, 176))
            resized_image.save(f, format=image_format)

        Screenshot.objects.create(film=film, file=file_name)

    # s3 files uploading

    # Credentials and session
    send_images_to_s3(file_dir, 'films-screenshots', film)
    send_images_to_s3(compressed_file_dir, 'films-compressed-screenshots', film)

    clear_directory(file_dir)
    clear_directory(compressed_file_dir)


def send_images_to_s3(directory, bucket, instance):
    """
    Sends images to given s3 bucket
    @param directory: path to directory with images
    @param bucket: s3 bucket name
    @param instance: model instance for getting 'pk' field
    """

    # Credentials and session
    aws_session = settings.AWS_SESSION
    s3 = aws_session.client('s3')

    for file in pathlib.Path(directory).iterdir():
        s3.upload_file(file.absolute(), bucket, f'{instance.pk}/{file.name}')


def clean_s3():
    """
    Cleans all s3 buckets when program starts
    """
    logger.debug('Connecting to Amazon S3...')
    aws_session = settings.AWS_SESSION

    s3_client = aws_session.client('s3')
    s3_resource = aws_session.resource('s3')

    for element in s3_client.list_buckets()['Buckets']:
        bucket = s3_resource.Bucket(element['Name'])
        bucket.objects.all().delete()
        logger.debug('Deleted all objects from "%s" bucket' % bucket.name)

    logger.debug('Successfully cleaned s3 data')


def clean_s3_model_data(instance: Model):
    """
    Cleans specific film / actor s3 data
    """

    # Initializing S3 session variables
    logger.info('Connecting to Amazon S3...')
    aws_session = settings.AWS_SESSION
    s3_resource = aws_session.resource('s3')

    if isinstance(instance, Film):
        screenshots_bucket = s3_resource.Bucket('films-screenshots')
        compressed_screenshots_bucket = s3_resource.Bucket('films-compressed-screenshots')

        # Deleting specific screenshots folder (e.g. '241/')
        deleted_screenshots = screenshots_bucket.objects.filter(Prefix='%s/' % instance.pk).delete()
        deleted_compressed_screenshots = compressed_screenshots_bucket.objects.filter(Prefix='%s/' % instance.pk).delete()

        logger.debug('Deleted screenshot objects: %s' % deleted_screenshots[0]['Deleted'])
        logger.debug('Deleted compressed screenshot objects: %s' % deleted_compressed_screenshots[0]['Deleted'])

    elif isinstance(instance, Actor):
        actors_bucket = s3_resource.Bucket('actors-screenshots')
        deleted_actors_screenshots = actors_bucket.objects.filter(Prefix='%s/' % instance.pk).delete()
        logger.debug('Deleted screenshot objects: %s' % deleted_actors_screenshots[0]['Deleted'])

    logger.info(f'Successfully cleaned {instance.__class__.__name__.lower()}s/{instance.pk} S3 data')


def create_directory(path: str):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def clear_directory(path: str):
    for file in pathlib.Path(path).iterdir():
        try:
            os.remove(file.absolute())
        except FileNotFoundError:
            pass

    try:
        os.rmdir(path)
    except FileNotFoundError:
        pass
