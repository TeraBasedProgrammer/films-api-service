from django.core.management.base import BaseCommand
import films.models as models
from films.services import clean_s3

import logging

logger = logging.getLogger('logger')


class Command(BaseCommand):
    def handle(self, *args, **options):

        # Retrieving all model classes of the project
        models_classes = dict([(name, cls) for name, cls in models.__dict__.items() if isinstance(cls, type)])

        # Cleaning all project's custom models (including s3 data)
        for key, value in models_classes.items():
            deleted_count, _ = value.objects.all().delete()
            logger.debug(f'Cleaned model "{key}". Objects deleted: {deleted_count}')
        clean_s3()
