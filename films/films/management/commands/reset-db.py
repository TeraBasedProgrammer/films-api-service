from django.core.management.base import BaseCommand
from django.conf import settings
import films.models as models
from films.services import clean_s3_model_data

import logging

logger = logging.getLogger('logger')


class Command(BaseCommand):
    def handle(self, *args, **options):

        # Retrieving all model classes of the project
        models_classes = dict([(name, cls) for name, cls in models.__dict__.items() if isinstance(cls, type)])

        # Cleaning all project's custom models (including s3 data)
        for key, value in models_classes.items():
            try:
                instances = value.objects.all()
                if not settings.DEBUG:
                    for instance in instances:
                        clean_s3_model_data(instance) 

                deleted_count, _ = instances.delete()
                logger.debug(f'Cleaned model "{key}". Objects deleted: {deleted_count}')
            except AttributeError:
                pass


