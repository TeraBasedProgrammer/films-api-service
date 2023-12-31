import logging

from django.conf import settings

from films.services import clear_directory, create_directory, send_images_to_s3

logger = logging.getLogger('logger')


def initialize_photo(photo_image, actor):
    if photo_image:
        logger.info(f'Preparing "{str(actor)}" photo to sending to S3...')
        file_dir = f'{settings.MEDIA_ROOT}/temp/{actor.slug}/'
        create_directory(file_dir)

        photo_file = f'{file_dir}photo.{actor.photo_format}'

        with open(photo_file, 'wb') as f:
            f.write(photo_image.file.read())

        send_images_to_s3(file_dir, 'actors-screenshots', actor)

        clear_directory(file_dir)



