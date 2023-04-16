from rest_framework.serializers import ValidationError
from django.core.validators import RegexValidator


def validate_age(value):
    if not 0 <= value <= 120:
        raise ValidationError('Age must be from 0 to 120')
    return value
