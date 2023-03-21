from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    def handle(self, *args, **options):
        Film.objects.all().delete()
