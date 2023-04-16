from films.services import create_directory, clear_directory, send_images_to_s3
from django.conf import settings


def initialize_photo(photo_image, actor):
    file_dir = f'{settings.MEDIA_ROOT}/temp/{actor.pk}/'
    create_directory(file_dir)

    photo_file = f'{file_dir}photo.{actor.photo_format}'

    with open(photo_file, 'wb') as f:
        f.write(photo_image.file.read())

    send_images_to_s3(file_dir, 'actors-screenshots', actor)



