from django.core.management.base import BaseCommand
import films.models as models
from films.services import clean_s3


class Command(BaseCommand):
    def handle(self, *args, **options):

        # Retrieving all model classes from films.models module
        models_classes = dict([(name, cls) for name, cls in models.__dict__.items() if isinstance(cls, type)])

        for key, value in models_classes.items():
            deleted_count, _ = value.objects.all().delete()
            print(f'Cleaned model {key}. Objects deleted: {deleted_count}')
        clean_s3()
