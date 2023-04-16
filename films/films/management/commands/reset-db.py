from django.core.management.base import BaseCommand
import films.models as models
from films.services import clean_s3

import logging

debug_logger = logging.getLogger('debug_django')


class Command(BaseCommand):
    def handle(self, *args, **options):

        # Retrieving all model classes of the project
        models_classes = dict([(name, cls) for name, cls in models.__dict__.items() if isinstance(cls, type)])
        for key, value in models_classes.items():
            deleted_count, _ = value.objects.all().delete()
            debug_logger.debug(f'Cleaned model {key}. Objects deleted: {deleted_count}')
        clean_s3()
