import json
import logging
import os
import pathlib
import shutil

import requests_cache
from actors.models import Actor
from django.conf import settings
from django.db.models import Model
from PIL import Image
from rest_framework.exceptions import APIException, ValidationError

from .models import Film, Screenshot

logger = logging.getLogger('logger')


def create_directory(path: str):
    logger.debug(f'Creating directory "{path}"...')
    try:
        logger.debug(f'Successfully created directory "{path}"')
        os.mkdir(path)
    except FileExistsError:
        logger.debug(f'FileExistsError - Directory "{path}" already exists')
        pass


def clear_directory(path: str):
    logger.debug(f'Cleaning directory "{path}"...')
    for file in pathlib.Path(path).iterdir():
        try:
            os.remove(file.absolute())
        except FileNotFoundError:
            pass

    try:
        os.rmdir(path)
    except FileNotFoundError:
        pass
    logger.debug(f'Successfully removed directory "{path}"')


def clean_temp():
    logger.debug(f'Cleaning directory "temp"...')
    for file in pathlib.Path(f'{settings.MEDIA_ROOT}/temp/').iterdir():
        try:
            shutil.rmtree(file.absolute())
        except FileNotFoundError:
            pass

    logger.debug(f'Successfully cleaned directory "temp"')


def create_screenshot_files(screenshot_data, i, file_dir, compressed_file_dir):
    """
    Creates screenshots images in temp folder
    @param screenshot_data: data of a single Base64 screenshot object
    @param i: Iterator for screenshot file naming
    @param file_dir: Screenshot file path in temp folder
    @param compressed_file_dir: Compressed screenshot file path in temp folder
    """
    image_data = screenshot_data.pop('image')

    image_format = image_data.content_type.split("/")[1]

    # Name of the file (e.g. 'screenshot-1.png')
    file_name = f'screenshot-{i + 1}.{image_format}'

    file_path = f'{file_dir}{file_name}'
    compressed_file_path = f'{compressed_file_dir}{file_name}'

    with open(file_path, 'wb') as f:
        f.write(image_data.file.read())

    with open(compressed_file_path, 'wb') as f:
        f.write(image_data.file.read())

        # Image compressing
        image = Image.open(file_path)
        image_size = image.size
        resized_width = round(image_size[0] * (176 / image_size[1]))
        resized_image = image.resize((resized_width, 176))

        resized_image.save(f, format=image_format)

    return file_name


def send_images_to_s3(directory, bucket, instance):
    """
    Sends images to given s3 bucket (if in prod mode)
    @param directory: path to directory with images
    @param bucket: s3 bucket name
    @param instance: model instance for getting 'slug' field
    """

    # Credentials and session
    aws_session = settings.AWS_SESSION
    s3 = aws_session.client('s3')

    if settings.DEBUG:
        logger.debug(f'App is in debug mode, nothing was actually sent to S3')
        return

    for file in pathlib.Path(directory).iterdir():
        s3.upload_file(file.absolute(), bucket, f'{instance.slug}/{file.name}')
        logger.debug(f'"{file.name}" file was successfully sent to S3')

    logger.info(f'All "{str(instance)}" files were successfully sent to S3')


def initialize_images(poster_image, screenshots_data, film):
    logger.info(f'Preparing "{str(film)}" images to sending to S3...')

    # Path to temp screenshots dir
    file_dir = f'{settings.MEDIA_ROOT}/temp/{film.slug}/'

    # Path to temp compressed screenshots dir
    compressed_file_dir = f'{file_dir[:-1]}-compressed/'

    # Creating film (slug) screenshots folder
    create_directory(file_dir)

    # Creating film (slug) compressed screenshots folder
    create_directory(compressed_file_dir)

    if poster_image:
        poster_file = f'{file_dir}poster.{film.poster_format}'
        poster_compressed_file = f'{file_dir}compressed-poster.{film.poster_format}'

        # Poster file creation
        with open(poster_file, 'wb') as f:
            f.write(poster_image.file.read())
            logger.info(f'Created "{str(film)}" film poster file')

        with open(poster_compressed_file, 'wb') as f:
            # Image compressing
            image = Image.open(poster_file)
            resized_image = image.resize((270, 400))

            resized_image.save(f, format=film.poster_format)
            logger.info(f'Created "{str(film)}" film compressed poster file')

    # Screenshots files creation
    if screenshots_data:
        if not film.screenshots.exists():
            for i, screenshot_data in enumerate(screenshots_data):
                file_name = create_screenshot_files(screenshot_data, i, file_dir, compressed_file_dir)

                Screenshot.objects.create(film=film, file=file_name)
                logger.info(f'Created "{file_name}" file')
        else:
            if len(screenshots_data) == len(film.screenshots.all()):
                for i, screenshot_data in enumerate(screenshots_data):
                    create_screenshot_files(screenshot_data, i, file_dir, compressed_file_dir)
            elif len(screenshots_data) > len(film.screenshots.all()):
                for i, screenshot_data in enumerate(screenshots_data):
                    file_name = create_screenshot_files(screenshot_data, i, file_dir, compressed_file_dir)
                    if i > len(film.screenshots.all()) - 1:
                        Screenshot.objects.create(film=film, file=file_name)
            else:
                film.screenshots.all().delete()
                clean_s3_model_data(film)
                for i, screenshot_data in enumerate(screenshots_data):
                    file_name = create_screenshot_files(screenshot_data, i, file_dir, compressed_file_dir)
                    Screenshot.objects.create(film=film, file=file_name)

    # s3 files uploading

    send_images_to_s3(file_dir, 'films-screenshots', film)
    send_images_to_s3(compressed_file_dir, 'films-compressed-screenshots', film)

    clear_directory(file_dir)
    clear_directory(compressed_file_dir)


def clean_s3():
    """
    Cleans all s3 buckets when program starts (DEBUG ONLY)
    """
    if not settings.DEBUG:
        return

    logger.debug('Connecting to Amazon S3...')
    aws_session = settings.AWS_SESSION

    s3_client = aws_session.client('s3')
    s3_resource = aws_session.resource('s3')

    for element in s3_client.list_buckets()['Buckets']:
        bucket = s3_resource.Bucket(element['Name'])
        bucket.objects.all().delete()
        logger.debug(f'Deleted all objects from "{bucket.name}" bucket')

    logger.debug('Successfully cleaned S3 data')


def clean_s3_model_data(instance: Model):
    """
    Cleans specific film / actor s3 data
    """
    if settings.DEBUG:
        logger.debug(f'App is in debug mode, nothing was actually deleted from S3')
        return

    logger.info('Connecting to Amazon S3...')
    aws_session = settings.AWS_SESSION
    s3_resource = aws_session.resource('s3')

    if isinstance(instance, Film):
        screenshots_bucket = s3_resource.Bucket('films-screenshots')
        compressed_screenshots_bucket = s3_resource.Bucket('films-compressed-screenshots')

        # Deleting specific screenshots folder (e.g. '241/')
        deleted_screenshots = screenshots_bucket.objects.filter(Prefix=f'{instance.slug}/').delete()
        deleted_compressed_screenshots = compressed_screenshots_bucket.objects.filter(Prefix=f'{instance.slug}/').delete()

        if deleted_screenshots and deleted_compressed_screenshots:
            logger.debug(f'Deleted screenshot objects: "{deleted_screenshots[0]["Deleted"]}"')
            logger.debug(f'Deleted compressed screenshot objects: "{deleted_compressed_screenshots[0]["Deleted"]}"')

    elif isinstance(instance, Actor):
        actors_bucket = s3_resource.Bucket('actors-screenshots')
        deleted_actors_screenshots = actors_bucket.objects.filter(Prefix=f'{instance.slug}/').delete()
        if deleted_actors_screenshots:
            logger.debug(f'Deleted screenshot objects: {deleted_actors_screenshots[0]["Deleted"]}')

    logger.info(f'Successfully cleaned "{instance.__class__.__name__.lower()}s/{instance.slug}" S3 data')
    